from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from .models import Issue, Vote
from .forms import IssueForm
from django.contrib.auth import login
from .forms import IssueForm, CustomUserCreationForm


# view for the dashboard

def dashboard(request):

    # filter/sort values from the URL (GET parameters)
    selected_category = request.GET.get('category', 'ALL')
    selected_status = request.GET.get('status', 'ALL')
    sort_by = request.GET.get('sort_by', 'most_recent')

    # Start building the main query 
    # Annotate gets the vote count for each issue
    all_issues = Issue.objects.annotate(vote_count=Count('votes'))

    # Apply filters 
    if selected_category != 'ALL':
        all_issues = all_issues.filter(category=selected_category)
        
    if selected_status != 'ALL':
        all_issues = all_issues.filter(status=selected_status)

    # Apply sorting 
    if sort_by == 'most_voted':
        # Order by the annotated vote_count, then by date as a tie-breaker
        all_issues = all_issues.order_by('-vote_count', '-created_at')
    else:
        # Default sort: most recent
        all_issues = all_issues.order_by('-created_at')

    # Get the counts (this runs *after* filtering) 
    total_issues_count = all_issues.count()
    # Note: For the top cards, we might want to show *total* counts regardless of filters.
    # Let's keep it simple for now: the counts will reflect the filtered list.
    reported_count = all_issues.filter(status='REPORTED').count()
    in_progress_count = all_issues.filter(status='IN_PROGRESS').count()
    resolved_count = all_issues.filter(status='RESOLVED').count()
    
    # Pass all the data to the template 
    context = {
        'issues': all_issues,
        'total_issues_count': total_issues_count,
        'reported_count': reported_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        
        #Add these to build the dropdowns 
        'status_choices': Issue.STATUS_CHOICES,
        'category_choices': Issue.CATEGORY_CHOICES,
        
        # --- Add these to remember the user's selection ---
        'selected_category': selected_category,
        'selected_status': selected_status,
        'selected_sort_by': sort_by,
    }
    
    return render(request, 'tracker/dashboard.html', context)


# view for the report issue 
@login_required
def report_issue(request):
    
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)

        if form.is_valid():
            new_issue = form.save(commit=False)
            new_issue.report = request.user 
            new_issue.save()
            return redirect('dashboard')
    else:
        form = IssueForm()

    context = {
        'form': form
    }
    return render(request, 'tracker/report_issue.html', context)


# view for issues detail
def issue_detail(request, issue_id):
    # database query
    issue = get_object_or_404(Issue, pk=issue_id)

    # Handle POST requests for status updates 
    if request.method == 'POST' and request.user.is_staff:
        # Get the new status from the submitted form data
        new_status = request.POST.get('status')
        # Check if the submitted status is a valid choice
        valid_statuses = [choice[0] for choice in Issue.STATUS_CHOICES]
        if new_status in valid_statuses:
            issue.status = new_status
            issue.save() # Save the change to the database
            # Redirect back to the same page to see the update
            return redirect('issue_detail', issue_id=issue.id)

    # passing the real issue obj to the template
    content = {
        'issue': issue
    }
    return render(request, 'tracker/issue_detail.html', content)

# vote feature implementation
@login_required
def vote_issue(request, issue_id):
    if request.method == 'POST':
        #get the issue object
        issue = get_object_or_404(Issue, pk=issue_id)
        # get the user
        user = request.user

        voted = False
        # checking if the user has already voted
        try:
            # try to find a vote by this user for this issue
            vote = Vote.objects.get(user=user, issue=issue)
            #if found, the user is un-voting, so delete the vote
            vote.delete()
            voted = False
        except Vote.DoesNotExist:
            # if not found, the user is voting, so create the vote
            Vote.objects.create(user=user, issue=issue)
            voted = True

        # vote count for the issue
        new_vote_count = issue.votes.count()

        # return a JSON response
        return JsonResponse({'count': new_vote_count, 'voted': voted})
    
    # if it's not a POST request, render it to dashboard

    return redirect('dashboard')

# Registration Function for new user
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # save the new user to the database
            login(request, user)  # this logs them in immediately
            return redirect('dashboard')   # send them to dashboard
    else:
        form = CustomUserCreationForm()   # show a blank form
    
    return render(request, 'tracker/register.html', {'form': form})
