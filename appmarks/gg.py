# # from django.utils import timezone
# # # from django.utils.timezone.now
# # from django.utils.timezone import now
# # from datetime import date
# # print(date.today)


# def tinhtienluong(**kwargs):
#     # print(kwargs['luongthang'])
#     # for i in kwargs.items():
#     for k in kwargs.items():
#         print(k)
#         # user.k=v
#         # print(k,)
#     # print()


# luong = {'luongthang': 10000000, 'luongthuong': 10000000}
# luong2 = dict(luongthang=10000000, luongthuong=1000000)
# tinhtienluong(**luong)
import decimal
a=decimal.Decimal(5.5)
b=4
print(type(a))
print(type(b))
print(a/b)



# full_name = 'Quách/Hùng/Nam'

# word = full_name.split('/', 1)
# print(word)


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
