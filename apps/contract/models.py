from django.db import models
from django.utils import timezone

# Define the User model
class User(models.Model):
    # This is a comment for the User model
    username = models.CharField(max_length=255, unique=True)
    # The email of the user, must be unique
    email = models.EmailField(unique=True)
    # The date the user joined, defaults to the current time
    date_joined = models.DateTimeField(default=timezone.now) 
    is_active = models.BooleanField(default=True)
    user_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'User'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

# Define the Quiz model
class Quiz(models.Model):
    # The title of the quiz
    quiz_title = models.CharField(max_length=255)
    # A brief description of the quiz
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    number_of_questions = models.PositiveIntegerField(default=10)
    model_name = models.CharField(max_length=255, null=True, blank=True)
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('Easy', 'Easy'),('Medium', 'Medium'),('Hard', 'Hard')],
        default='Medium'
    )
    category = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)
    is_supervised = models.BooleanField(default=False)
    is_organization_only = models.BooleanField(default=False)
    is_timed = models.BooleanField(default=False)
    time_limit = models.FloatField(null=True, blank=True)
    auth_required = models.BooleanField(default=False)
    has_flash_card = models.BooleanField(default=False)
    is_global = models.BooleanField(default=False)

    def __str__(self):
        return self.quiz_title

    class Meta:
        db_table = 'Quiz'
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

# Define the Question model
class Question(models.Model):
    # The quiz to which this question belongs
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    # The text of the question
    text = models.TextField()

    def __str__(self):
        return self.text
    
    class Meta:
        db_table = 'question'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

# Define the AnswerOption model
class AnswerOption(models.Model):
    # The question to which this answer option belongs
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    # The label of the answer option, e.g., A, B, C
    label = models.CharField(max_length=1)  # A, B, C, etc.
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.label}: {self.text}"
    
    class Meta:
        db_table = 'answer_option'
        verbose_name = 'Answer Option'
        verbose_name_plural = 'Answer Options'

class QuizSubmission(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='authored_submissions')
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True)
    quiz_title = models.CharField(max_length=255)
    candidate_name = models.CharField(max_length=255)
    candidate_id = models.IntegerField()
    completion_date = models.DateTimeField(auto_now_add=True)
    percentage_score = models.IntegerField()
    number_of_correct = models.IntegerField()
    total_number_of_questions = models.IntegerField()

    def __str__(self):
        return f"Result for {self.candidate_name} - {self.percentage_score}%"
    
    class Meta:
        db_table = 'quiz_submission'
        verbose_name = 'Quiz Submission'
        verbose_name_plural = 'Quiz Submissions'

class QuizResultSnapshot(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    quiz_id = models.IntegerField()
    quiz_title = models.CharField(max_length=255)
    quiz_submission_id = models.IntegerField()
    quiz_category = models.CharField(max_length=255)
    quiz_creator_name = models.CharField(max_length=255)
    quiz_creator_id = models.IntegerField()
    completion_date = models.DateTimeField(auto_now_add=True)
    percentage_score = models.IntegerField()
    number_of_correct = models.IntegerField()
    total_number_of_questions = models.IntegerField()

    def __str__(self):
        return f"Result for {self.candidate} - {self.percentage_score}%"
    
    class Meta:
        db_table = 'quiz_result_snapshot'
        verbose_name = 'Quiz Result Snapshot'
        verbose_name_plural = 'Quiz Result Snapshots'

class TestResponse(models.Model):
    quiz_submission = models.ForeignKey(QuizSubmission, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, related_name='authored_test_responses', on_delete=models.SET_NULL, null=True, blank=True)
    candidate = models.ForeignKey(User, related_name='candidate_test_responses', on_delete=models.SET_NULL, null=True, blank=True)
    question = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    selected_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"Response for submission {self.quiz_submission_id}"
    
    class Meta:
        db_table = 'test_response'
        verbose_name = 'Test Response'
        verbose_name_plural = 'Test Responses'

class Flashcard(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    number_of_flashcards = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='flashcards'
    )
    quiz = models.OneToOneField(
        Quiz,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='flashcard'
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'flashcard'
        verbose_name = 'Flashcard'
        verbose_name_plural = 'Flashcards'

class FlashcardItem(models.Model):
    flashcard = models.ForeignKey(
        Flashcard,
        on_delete=models.CASCADE,
        related_name='items'
    )
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f"{self.question[:50]}..."

    class Meta:
        db_table = 'flashcard_item'
        verbose_name = 'Flashcard Item'
        verbose_name_plural = 'Flashcard Items'

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration_days = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'SubscriptionPlan'
        verbose_name = 'SubscriptionPlan'
        verbose_name_plural = 'SubscriptionPlans'

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'UserSubscription'
        verbose_name = 'UserSubscription'
        verbose_name_plural = 'UserSubscriptions'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.lastname

    class Meta:
        db_table = 'UserProfile'
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfile'



class UserFeedback(models.Model):
    FEEDBACK = 'FB'
    COMPLAINT = 'CP'
    ISSUE_TYPE_CHOICES = [(FEEDBACK, 'Feedback'), (COMPLAINT, 'Complaint')]
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    issue_type = models.CharField(max_length=2,choices=ISSUE_TYPE_CHOICES,help_text="Select if feedback or complaint")
    public_display = models.BooleanField(default=False,help_text="Display feedback publicly")
    title = models.CharField(max_length=255)
    rating = models.IntegerField(default=0,help_text="Numeric rating")
    message = models.TextField()
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_issue_type_display()})"

    class Meta:
        db_table = 'UserFeedback'
        verbose_name = 'UserFeedback'
        verbose_name_plural = 'UserFeedbacks'



class QuizFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,help_text="The user providing the feedback.")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,help_text="The quiz being reviewed.")
    title = models.CharField(max_length=255)
    message = models.TextField(help_text="Text feedback on the quiz.")
    rating = models.IntegerField(default=0,help_text="Optional numeric rating for the quiz.")
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback by {self.user} on {self.quiz} - Rating: {self.rating}"
    
    class Meta:
        db_table = 'QuizFeedback'
        verbose_name = 'Quiz Feedback'
        verbose_name_plural = 'Quiz Feedbacks'