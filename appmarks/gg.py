# # from django.utils import timezone
# # # from django.utils.timezone.now
# # from django.utils.timezone import now
# # from datetime import date
# # print(date.today)


# aa={"name":"Name","tuoi":"19"}
# xx=aa.get('ho')
# print(xx)
# print(aa)

# class FormTeacher(UserCreationForm):
#     phone_number = forms.CharField(max_length=32)

#     def save(self, commit=True):
#         instance = super().save(commit=True)
#         teacher = Teacher(
#             user=instance, phone_number=self.cleaned_data['phone_number'])
#         teacher.save()
#         return instance




# class UserWithProfileAdmin(BaseUserAdmin):
#     add_form = FormTeacher
#     add_fieldsets = (
#         (None, {
         
#             # add any custom fields here
#             'fields': ('username',),
#         }),
#     )


# admin.site.register(UserWithProfileAdmin)

# class TeacherForm(UserCreationForm):
#     # supervisor = forms.ModelChoiceField(queryset=User.objects)
#     class Meta:

#         model = CustomUser
#         # fields = ('department', 'user')

#     # def save(self, commit=True):
#     #     supervisor = self.cleaned_data['supervisor']
#     #     # Save user first
#     #     user = super(MyTestForm, self).save(commit=True)
#     #     profile = Profile.objects.create(user=user)
#     #     profile.supervisor = supervisor
#     #     profile.save()
#     #     return user


# class MyTeacherAdmin(BaseUserAdmin):
#     add_form = TeacherForm
#     form = TeacherForm
#     add_fieldsets = (
#         (None, {
#             'fields': ('department',)
#         }),
#     )