from django.shortcuts import render,redirect


from django.views.generic import View

from budget.forms import ExpenseForm,IncomeForm,RegistrationForm,LoginForm

from budget.models import Expense,Income

from django.contrib import messages

from django.utils import timezone

from django.db.models import Sum

from budget.decorators import signin_required

from django.utils.decorators import method_decorator

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout


# Create your views here.


@method_decorator(signin_required,name="dispatch")
class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):

        if not request.user.is_authenticated:

            messages.error(request,"login before ")

            return redirect("signin")

        form_instance=ExpenseForm()

        qs=Expense.objects.all()

        # income_instance=IncomeForm()

        # qs_income=Income.objects.all()

        return render(request,"expense_add.html",{"form":form_instance,"data":qs})
    
    def post(self,request,*args,**kwargs):

        form_instance=ExpenseForm(request.POST)

        if form_instance.is_valid():
            
            form_instance.instance.user_object=request.user

            form_instance.save()

            messages.success(request,"message saved success")

            print("expense is added")

            return redirect("expense-add")
        
        else:

            return render(request,"expense_add.html",{"form":form_instance})


@method_decorator(signin_required,name="dispatch")
class ExpenseUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_object=Expense.objects.get(id=id)

        form_instance=ExpenseForm(instance=expense_object) 

        return render(request,"expense_edit.html",{"form":form_instance})  

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_object=Expense.objects.get(id=id)

        form_instance=ExpenseForm(instance=expense_object,data=request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"update success")

            return redirect("expense-add")
        
        else:

            messages.error(request,"not update, error")

            return render(request,"expense_add.html",{"form":form_instance})


@method_decorator(signin_required,name="dispatch")
class ExpenseDetailView(View):

    def get(self,request,*args,**kwargs):

        id =kwargs.get("pk")

        qs=Expense.objects.get(id=id)

        return render(request,"expense_detail.html",{"data":qs})


@method_decorator(signin_required,name="dispatch")
class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Expense.objects.get(id=id).delete()

        messages.success(request,"table has been deleted")

        redirect("expense-add")


@method_decorator(signin_required,name="dispatch")
class ExpenseSummaryView(View):

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year= timezone.now().year

        expense_list=Expense.objects.filter(created_date__month=current_month,
                                            created_date__year=current_year)
        
        expense_total=expense_list.values("amount").aggregate(total=Sum("amount"))

        print(expense_total)

        category_summary=expense_list.values("category").annotate(total=Sum("amount"))

        print(category_summary)

        priority_summary=expense_list.values("priority").annotate(total=Sum("amount"))

        print(priority_summary)


        data={
            "expense_total":expense_total,
            "category_summary":category_summary,
            "priority_summary":priority_summary,
        }

        return render(request,"expense_summary.html",data)


@method_decorator(signin_required,name="dispatch")
class IncomeCreateView(View):

    def get(self,request,*args,**kwargs):

        income_instance=IncomeForm()

        qs_income=Income.objects.all()

        return render(request,"income_add.html",{"form_in":income_instance,"data":qs_income})
    
    def post(self,request,*args,**kwargs):

        income_instance=IncomeForm(request.POST)

        if income_instance.is_valid():

            income_instance.save()

            return redirect("income-add")

        else:

            render(request,"income_add.html",{"form_in":income_instance})


@method_decorator(signin_required,name="dispatch")
class IncomeUpdateView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        inc_obj=Income.objects.get(id=id)

        form_instance=IncomeForm(instance=inc_obj)

        return render(request,"income_update.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        inc_obj=Income.objects.get(id=id) 

        form_instance=IncomeForm(instance=inc_obj,data=request.POST)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("income-add")
        
        else:

            return render(request,"income_add.html",{"form":form_instance})


@method_decorator(signin_required,name="dispatch")
class IncomeDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Income.objects.get(id=id).delete()

        form_instance=IncomeForm()

        return redirect("income-add")
    
    # def post(self,request,*args,**kwargs):

    #     def get(self,request,*args,**kwargs):

    #     id=kwargs.get("pk")

    #     Income.objects.get(id=id).delete()

    #     form_instance=IncomeForm(request.POST)

    #     return redirect("income-add")


@method_decorator(signin_required,name="dispatch")
class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,"register.html",{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            data = form_instance.cleaned_data

            User.objects.create_user(**data) 


            return redirect("signup")
        else:
            return render(request,"register.html",{"form":form_instance})


@method_decorator(signin_required,name="dispatch")        
class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=LoginForm()

        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=LoginForm(request.POST)
       
        if form_instance.is_valid():
           
           data=form_instance.cleaned_data

           uname=data.get("username")

           pwd=data.get("password")

           user_object=authenticate(request,username=uname,password=pwd)

           if user_object:
               
               login(request,user_object)

               return redirect("dashboard")
        
        messages.error(request,"invalid credential")

        return render(request,"login.html",{"form":form_instance})


@method_decorator(signin_required,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
    

class DashBoardView(View):

    def get(request,self,*args,**kwargs):


        current_month=timezone.now().month

        current_year=timezone.now().year

        expense_list=Expense.objects.filter(user_object=request.user,created_date__month=current_month,created_date__year=current_year)

        income_list=Income.objects.filter(user_object=request.user,created_date__month=current_month,created_date__year=current_year)

        print("expense list",expense_list)

        print("income list",income_list)

        expense_total=expense_list.values("amount").aggregate(total=Sum("amount"))
        
        income_total=income_list.values("amount").aggregate(total=Sum('amount'))

        print("expense total",expense_total)

        print("income total",income_total)
        
        return render(request,"board.html")


