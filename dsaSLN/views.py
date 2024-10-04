import json
from django.conf import settings
from django.shortcuts import get_object_or_404, render,redirect
import requests


from .models import *
from django.http import HttpResponse
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.paginator import *
from django.views.decorators.csrf import csrf_exempt
from concurrent.futures import ThreadPoolExecutor
# from Comisiions.views import viewComissions


# Create your views here.
@csrf_exempt
def dsaLogin(request):
   print("hghDsaLogin.........")
   if request.method=="POST":
      print("888888888888888.........")
      print(request.POST.get('applicationid'))
      if request.POST.get('applicationid')=="SLNDSA1003":
         request.session['verified']=True
         request.session['dsaLoginId']=request.POST.get('applicationid')
         
         if request.session.get('indexPage'): return redirect('dsa-index')
         
         return redirect(request.session.get('pageurl'))

   return render(request,'dsaLogin.html')

def dsaLogout(request):
   if  request.session.get('verified'):
    del request.session['verified']
   if request.session.get('indexPage'):
     del request.session['indexPage']
   return render(request,'dsaLogin.html')


# DSA ManualId
def dsamanualId(request):
   print(request.session.get('dsaLoginId'))
   return request.session.get('dsaLoginId')
# DSA ManualId

@csrf_exempt
def dsaProfile(request):
    resp=requests.get(f'http://127.0.0.1:999/api/mymodel/{dsamanualId(request)}/custom_get/')
    if resp.status_code==200:
       print("json data")
       print(resp.json())
       data=resp.json()
             
       if request.method=='POST':
          
          request.POST.get('dsa_registerid')
          
          data={
             
             'dsa_name':request.POST.get('dsa_name'),
             'dsa_password':request.POST.get('dsa_password')
             
          }
          print(data)
          print("ipouy")
          response=requests.post(f'http://127.0.0.1:999/api/mymodel/{dsamanualId(request)}/custom_update/',json=data)
          if response.status_code==201 or response.status_code==200:
            data=response.json()
            print("jsonpost")
            listData=[data]
            print(listData)
            return render(request,'DSAProfile.html',{'data':listData,'edited':True})
          else:
             return HttpResponse("No data..")
          
          
       return render(request,'DSAProfile.html',{'data':data})

         
    else: return None
    

def dsaDashboard(request):
    return render(request,"DsaDashboard.html")


def disbursedTotalAmount(request):
   request.session['disbursedTotalAmount']=True
   from Comisiions.views import commonComissions
   total=commonComissions(request)
   if total:
      loans= total
      request.session['disbursedTotalAmount']=None
      del request.session['disbursedTotalAmount']
      return loans
   else:
      return None
   
def disbursedTotalLoans(request):
   request.session['disbursedTotalLoans']=True
   from Comisiions.views import commonComissions
   total=commonComissions(request)
   if total:
      loans= total
      request.session['disbursedTotalLoans']=None
      del request.session['disbursedTotalLoans']
      return loans
   else:
      return None
   
def disbursedTotalLoanIds(request):
  response=requests.get(f"{settings.ACCOUNTS_SOURCE_URL}/getDisburseIds/{dsamanualId(request)}")
  if response.status_code==200:
     res=response.json()
     finlres=[res]
     print(res)
     return res
  else:
     return None
  
def demo4(request):
     return HttpResponse(f"{settings.ACCOUNTS_SOURCE_URL}")

# Insurance..........................................
def lifeInsurance(request):
   return render(request,"Lifeinsurance.html",{'url':f"{settings.SOURCE_PROJECT_URL}"})

def generalInsurance(request):
   return render(request,"GeneralInsurance.html",{'url':f"{settings.SOURCE_PROJECT_URL}"})

def healthInsurance(request):
   return render(request,"HealthInsurance.html",{'url':f"{settings.SOURCE_PROJECT_URL}"})

def allInsurance(request):
   return render(request,"AllInsurance.html",{'url':f"{settings.SOURCE_PROJECT_URL}"})

# Insurance............................................



# CheckEligibility.....................
def educheckEligible(request):
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/el/edubasicdetail/"})

def busicheckEligible(request):
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/bl/busbasicdetail/"})

def lapcheckEligible(request):
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/basicdetail/"})

def homecheckEligible(request):
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/pl/hlbasicdetail/"})

def personalcheckEligible(request):
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/pl/plbasicdetail/"})

def carcheckEligible(request):
   print(f"{settings.SOURCE_PROJECT_URL}cl/carbasic-details/")
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/cl/carbasic-details/"})

def creditcheckEligible(request):
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/cc/crebasicdetail/"})

def goldcheckEligible(request):
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/goldbasicdetail/"})



# CheckEligibility.....................


def dsaTotalAllApplications(request):
    dsaObj = DSA.objects.prefetch_related('dsa').get(dsa_registerid=dsamanualId(request))
    dsaApp=dsaObj.dsa.all()
    return dsaApp
   
# def chat(request):
#     return render(request,"chat.html") 

# Business LOan API......................................................
def businessLoanApi(request):
    #  print(f'{settings.SOURCE_PROJECT_URL}/bl/getByRefCode/SLNDSA1002')
     records=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/getByRefCode/{dsamanualId(request)}')
     if records.status_code==200:
      res=records.json()
      # loans=[]
      # allLoans=[]
      if request.session.get('approved') == "Approved":
         responseData=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/getApprovedRecords/{dsamanualId(request)}')
         if responseData.status_code==200:
            res=responseData.json()
            # print(result)            
         else:
            print("else PArt../")
            return []
         
         # Old Approach
      #  print("Apprved method..")
      #  for result in res:
      #     if result.get('applicationverification') is not None:
      #        a=result.get('applicationverification')
      #        if a.get('verification_status')=="Approved":
      #           loans.append(result)
      #  return loans

      
      if request.session.get('rejected') == "Rejected":
         responseData=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/getRejectedRecords/{dsamanualId(request)}')
         if responseData.status_code==200:
            res=responseData.json()           
         else:
            # print("else PArt../")
            return []
         
      #   del request.session['approved']
      #   for result in res:
      #     if result.get('verification') is not None:
      #        a=result.get('verification')
      #        print(result.get('verification'),"09iiiiiiiiiiiii")
      #        if a.get('verification_status')=="Rejected":
      #           loans.append(result)
      #   return loans
      
      
    #Business Total Loans
      return res
     else:
         return []
     
     
# Education LOan API......................................................
def educationLoanApi(request):
    print("Education loan/..............................")
    records=requests.get(f'{settings.SOURCE_PROJECT_URL}/el/getByRefCode/{dsamanualId(request)}')
    if records.status_code==200:
      print("edu../")
      res=records.json()
     
      loans=[]
      allLoans=[]
     
      if request.session.get('approved') == "Approved":
      
       for result in res:
          if result.get('verification') is not None:
             a=result.get('verification')
             if a.get('verification_status')=="Approved":
                loans.append(result)
       return loans
    
      if request.session.get('rejected') == "Rejected":
      #   del request.session['approved']
        for result in res:
          if result.get('verification') is not None:
             a=result.get('verification')
             print(result.get('verification'),"09iiiiiiiiiiiii")
             if a.get('verification_status')=="Rejected":
                loans.append(result)
        return loans
      
    #Education Total Loans
      print(res)
      return res
    else:
         return []
      
def lapApi(request):
   #  print("Education loan/..............................")
    records=requests.get(f'{settings.SOURCE_PROJECT_URL}/lapapi/{dsamanualId(request)}/getByRefCode/')
    if records.status_code==200:
      # print("edu../")
      res=records.json()
     
      loans=[]
      allLoans=[]
     
      if request.session.get('approved') == "Approved":
      
       for result in res:
          if result.get('verification') is not None:
             a=result.get('verification')
             if a.get('verification_status')=="Approved":
                loans.append(result)
       return loans
    
      if request.session.get('rejected') == "Rejected":
      #   del request.session['approved']
        for result in res:
          if result.get('verification') is not None:
             a=result.get('verification')
             print(result.get('verification'),"09iiiiiiiiiiiii")
             if a.get('verification_status')=="Rejected":
                loans.append(result)
        return loans
      
    #Education Total Loans
      print(res)
      return res
    else:
         return []
   
      
def dsaAllInsurancesCount(request):
   response=requests.get(f"{settings.SOURCE_PROJECT_URL}/commonInsuranceGet/{dsamanualId(request)}")
   if response.status_code==200:
      print(response.json())
      return response.json()
   else:
      return HttpResponse(response.content,response.status_code)
   
def creditCardCount(request,refCode):
    dsaObj = DSA.objects.prefetch_related('dsa').get(dsa_registerid=refCode)
    dsaApp=dsaObj.dsa.all()
    result=[]
    for i in dsaApp:
       if i.cust_applicationId.startswith('SLNCC'):
          result.append(i.cust_applicationId)
    return len(result)
 
def allCount(request,refCode):
    dsaObj = DSA.objects.prefetch_related('dsa').get(dsa_registerid=refCode)
    dsaApp=dsaObj.dsa.all()
    result,busines,education,personal,home,lap,car=[],[],[],[],[],[],[]
    
    for i in dsaApp:
       if i.cust_applicationId.startswith('SLNCC'):
          result.append(i.cust_applicationId)
          
       elif i.cust_applicationId.startswith('SLNBL'):
          busines.append(i.cust_applicationId)
      
       elif i.cust_applicationId.startswith('SLNEL'):
          education.append(i.cust_applicationId)
          
       elif i.cust_applicationId.startswith('SLNPL'):
          personal.append(i.cust_applicationId)
          
       elif i.cust_applicationId.startswith('SLNHL'):
          home.append(i.cust_applicationId)
         
       elif i.cust_applicationId.startswith('SLNLAP'):
          lap.append(i.cust_applicationId)
          
       elif i.cust_applicationId.startswith('SLNCL'):
          car.append(i.cust_applicationId)
         
    context={
       'totalApplications':len(dsaApp),
       'creditCard':len(result),
       'businessLength':len(busines),
       'EducationLength':len(education),
       'personalLength':len(personal),
       'homeLength':len(home),
       'carLength':len(car),
       'lapLength':len(lap),
       'Insurances':dsaAllInsurancesCount(request),
   }
    return context
       
   

#DSA Index MEthod.................................................
def dsaIndex(request):
    totalApplications=dsaTotalAllApplications(request)

    education=[]
    personal=[]
    request.session['common']="business"
    # busi=businessLoanApi(request)

    # bus=businessLoanApi(request)
    return render(request,"DSAIndex.html",allCount(request,dsamanualId(request)))



# Approved Loans Method.............................................
@csrf_exempt
def approvedLoans(request):
  if request.method=='POST':
     if request.POST.get('loantype'):

      if request.POST.get('date'):
      #   print(request.POST.get('date'))
        request.session['startdate']=request.POST.get('date').split(' to ')[0]
        request.session['enddate']=request.POST.get('date').split(' to ')[1]
      else:
        request.session['startdate']=None
        # print( request.POST.get('loantype'))

      loantyp=request.POST.get('loantype')
        # date= request.POST.get('date')
      if request.POST.get('loantype')!='All':
         request.session['loantype']=loantyp
         
         # print(loantyp + "hhhhhoop")
         if request.session.get('All'):
          del request.session['All']
        
      else:
            request.session['All']=loantyp
            if request.session.get('loantype'):
             del request.session['loantype']

# search By Application Id
     if request.POST.get('applicationid'):
      request.session['applicationid']=request.POST.get('applicationid')
      # print(request.POST.get('applicationid')+ "jjjjkk111")
      if request.session.get('loantype') or request.session.get('All'):
         request.session['All']=None
         request.session['loantype']=None
     else:
        request.session['applicationid']=None
        
# search By Application Id
     
  filterLoans=[]
  request.session['approved'] = "Approved"
  allLoans = []
  
     # For TO MAKE EXECUTION TIME LESS..
  with ThreadPoolExecutor() as executor:
        future_business = executor.submit(businessLoanApi, request)
        future_education = executor.submit(educationLoanApi, request)
        future_lap=executor.submit(lapApi,request)

        
  business_result = future_business.result()
  education_result = future_education.result()
  lap_result = future_lap.result()
      
  if business_result:
            allLoans.extend(business_result)
  if education_result:
            allLoans.extend(education_result)
  if lap_result:
     allLoans.extend(lap_result)


#   bus_loan_data = businessLoanApi(request)
#   edu_loan_data=educationLoanApi(request)
  
  del request.session['approved']
    
    # Check if loan_data is a list and extend allLoans, else append it directly
#   if bus_loan_data:
#      allLoans.extend(bus_loan_data)
#     #  print(allLoans)
#   if edu_loan_data:
#         allLoans.extend(edu_loan_data)

  totalLoanAmount=0
  if allLoans:
      
      
      request.session['approvedLoansLength']=len(allLoans)
      print("From Approved Loans...")
      if request.session.get('FromalloanstoApproved'):
       for amount in allLoans:
         # print(amount)
         totalLoanAmount+=float(amount.get('required_loan_amount'))
         # print(int(amount.get('required_loan_amount')))

      # print(totalLoanAmount)
       request.session['approvedLoansAmount']=totalLoanAmount
       return 
  
 
   
  print("From Aproved Nxt...")
  if request.session.get('applicationid'):
       for loans in allLoans:
          if loans.get('application_id')== request.session.get('applicationid'):
             filterLoans.append(loans)
      #  print("(0000000000)")

       if not filterLoans:
          request.session['applicationid']=None
          return render(request,'DataTable.html',{'objects': []})
       allLoans=filterLoans



  if request.session.get('loantype'):
     for loans in allLoans:
      #   print("NotAllLoans///////")
      #   print(loans.get('created_at'))
        if  request.session.get('startdate') and loans.get('application_loan_type')==request.session.get('loantype') and loans.get('created_at') >= request.session.get('startdate') and loans.get('created_at') <= request.session.get('enddate'):
           filterLoans.append(loans)
           
        if not request.session.get('startdate') and loans.get('application_loan_type')==request.session.get('loantype'):
           filterLoans.append(loans)
     allLoans=filterLoans
 
#   print(allLoans)
  if request.session.get('All'):
     for loans in allLoans:
      #   print("AllLoans")
      #   print(loans.get('created_at'))

        if  request.session.get('startdate') and loans.get('created_at') >= request.session.get('startdate') and loans.get('created_at') <= request.session.get('enddate'):
           filterLoans.append(loans)
        if not request.session.get('startdate'):
           filterLoans.append(loans)
     allLoans=filterLoans
     
  if allLoans:
    
     paginator = Paginator(allLoans, 1)  
     page = request.GET.get('page') 
     try:
        objects = paginator.page(page)
     except :
        objects = paginator.page(1)
        
    
     start_index = (objects.number - 1) * paginator.per_page + 1
   #   print(f"{objects.number}---{paginator.per_page}")



     if request.session.get('applicationid'):
       request.session['applicationid']=None
      #  print(allLOans)
       return render(request,'DataTable.html',{'objects': objects,'start_index': start_index})


   #    # Check if the request is an AJAX request
   #   if request.headers.get('x-requested-with') == 'XMLGetHttpRequest':
   #      print("Ajex method is activate..........")
   #      return render(request,'AllAprovedLoans.html',{'objects': objects,'start_index': start_index})


     return render(request, "AllAprovedLoans.html", {'objects': objects, 'start_index': start_index,'title':"Approved Loans"})
  else:
     return render(request, "AllAprovedLoans.html", {'objects': [],'title':"Approved Loans"})
  

# Rejected Loans.......................................................
@csrf_exempt
def rejectedLoans(request):
  if request.method=='POST':
     if request.POST.get('loantype'):

      if request.POST.get('date'):
      #   print(request.POST.get('date'))
        request.session['startdate2']=request.POST.get('date').split(' to ')[0]
        request.session['enddate2']=request.POST.get('date').split(' to ')[1]
      else:
        request.session['startdate2']=None
        # print( request.POST.get('loantype'))

      loantyp=request.POST.get('loantype')
        # date= request.POST.get('date')
      if request.POST.get('loantype')!='All':
         request.session['loantype2']=loantyp
         if request.session.get('All2'):
          del request.session['All2']
        
      else:
            request.session['All2']=loantyp
            if request.session.get('loantype2'):
             del request.session['loantype2']

      
# search By Application Id
     if request.POST.get('applicationid'):
       request.session['applicationid1']=request.POST.get('applicationid')
      #  print(request.POST.get('applicationid')+ "jjjjkk111")
       if request.session.get('loantype2') or request.session.get('All2'):
         request.session['All2']=None
         request.session['loantype2']=None
     else:
        request.session['applicationid1']=None
# search By Application Id

           
  filterLoans=[]
  request.session['rejected'] = "Rejected"
  allLoans = []
  
     # For TO MAKE EXECUTION TIME LESS..
  with ThreadPoolExecutor() as executor:
        future_business = executor.submit(businessLoanApi, request)
        future_education = executor.submit(educationLoanApi, request)
        future_lap=executor.submit(lapApi,request)

        
  business_result = future_business.result()
  education_result = future_education.result()
  lap_result = future_lap.result()
      
  if business_result:
            allLoans.extend(business_result)
  if education_result:
            allLoans.extend(education_result)
  if lap_result:
     allLoans.extend(lap_result)

#   bus_loan_data = businessLoanApi(request)
#   edu_loan_data=educationLoanApi(request)
  del request.session['rejected']
    
    # Check if loan_data is a list and extend allLoans, else append it directly
#   if bus_loan_data:
#      allLoans.extend(bus_loan_data)
#     #  print(allLoans)
#   if edu_loan_data:
#         allLoans.extend(edu_loan_data)

# For counting Rejected Loans
  totalLoanAmount=0
  if allLoans:
      request.session['rejectedLoansLength']=len(allLoans)
      # print(len(allLoans))
      print("From Rejected Loans........")
      if request.session.get('FromalloanstoRejectd'):
       for amount in allLoans:
         print(amount)
         totalLoanAmount+=float(amount.get('required_loan_amount'))
         # print(int(amount.get('required_loan_amount')))

      # print(totalLoanAmount)
       request.session['rejectedLoansAmount']=totalLoanAmount
       return 
      


# For counting Rejected Loans
  print("Nxt rEjected")
  if request.session.get('applicationid1'):
       for loans in allLoans:
          if loans.get('application_id')== request.session.get('applicationid1'):
             filterLoans.append(loans)
      #  print("(0000000000)")
      #  del request.session['applicationid1']
       if not filterLoans:
          request.session['applicationid1']=None
          return render(request,'DataTable.html',{'objects': []})
       allLoans=filterLoans

# Filters
  if request.session.get('loantype2'):
     for loans in allLoans:
      #   print("NotAllLoans")
      #   print(loans.get('created_at'))
        if  request.session.get('startdate2') and loans.get('application_loan_type')==request.session.get('loantype2') and loans.get('created_at') >= request.session.get('startdate2') and loans.get('created_at') <= request.session.get('enddate2'):
           filterLoans.append(loans)
             
        if not request.session.get('startdate2') and loans.get('application_loan_type')==request.session.get('loantype2'):
           filterLoans.append(loans)
     allLoans=filterLoans

  if request.session.get('All2'):
     for loans in allLoans:
      #   print("AllLoans")
      #   print(loans.get('created_at'))

      #   if  loans.get('created_at') >= request.session.get('startdate') and loans.get('created_at') <= request.session.get('enddate'):
      #      filterLoans.append(loans)
      #   if not request.session.get('startdate') and loans.get('loan_type')==request.session.get('loantype'):
      #      filterLoans.append(loans)
        if  request.session.get('startdate2') and loans.get('created_at') >= request.session.get('startdate2') and loans.get('created_at') <= request.session.get('enddate2'):
           filterLoans.append(loans)
        if not request.session.get('startdate2'):
           filterLoans.append(loans)
     allLoans=filterLoans
# Filters  


  if allLoans:
    #  print(allLoans)
    
     paginator = Paginator(allLoans, 1)
     page = request.GET.get('page') 
    
     try:
        objects = paginator.page(page)
     except :
        objects = paginator.page(1)
    
        
    
     start_index = (objects.number - 1) * paginator.per_page + 1
   #   print(f"{objects.number}---{paginator.per_page}")


     if request.session.get('applicationid1'):
       request.session['applicationid1']=None
      #  print(allLOans)
       return render(request,'DataTable.html',{'objects': objects,'start_index': start_index})


      # Check if the request is an AJAX request
     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      #   print("Ajex method is activate..........")
        return render(request,'AllAprovedLoans.html',{'objects': objects,'start_index': start_index})

     return render(request, "AllAprovedLoans.html", {'objects': objects, 'start_index': start_index,'title':"Rejected Loans"})
  else:
     return render(request, "AllAprovedLoans.html", {'objects': [],'title':"Rejected Loans"})
  
 
def get_all_dataAsJson(request):
   # print(dsamanualId(request))
   data=DSA.objects.prefetch_related('dsa').get(dsa_registerid=dsamanualId(request))
   
   data1=data.dsa.values()
   # print(data.dsaapp.all())
   return JsonResponse(list(data1),safe=False)

# ApplyForms.................................................................

def apply_business(request):
    return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/bl/demo",'dsaId':dsamanualId(request)})
def apply_Education(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/el/apply-educationalLoan",'dsaId':dsamanualId(request)})
def home_loan(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/pl/home/",'dsaId':dsamanualId(request)})
def credit_card(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/cc/credit/",'dsaId':dsamanualId(request)})
def car_loan(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/cl/car-loan-application/",'dsaId':dsamanualId(request)})
def lap(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/lapapply/",'dsaId':dsamanualId(request)})
def apply_personal(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/pl/personal/",'dsaId':dsamanualId(request)})
def apply_gold(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/goldloan/",'dsaId':dsamanualId(request)})




# All Loans......................................................................
@csrf_exempt
def allLOans(request):

   if request.GET.get('id'):
        template="DemowithOutDashBoard.html"
        an=990
   else:
        an=None
        template="DsaDashboard.html"


   
   # request.session['approved'] = None
   if request.method=='POST':
    
     if request.POST.get('loantype'):
        print(request.POST.get('loantype'),"000000000008776")
        if request.POST.get('loansteps'):
         #   print(request.POST.get('loansteps'))
           request.session['loansteps']=request.POST.get('loansteps')
        else:
            if request.session.get('loansteps'):
               del request.session['loansteps']
            
       
      #   print(request.POST.get('date'))
        if request.POST.get('date'):
         # print(request.POST.get('date'))
         request.session['startdate1']=request.POST.get('date').split(' to ')[0]
         request.session['enddate1']=request.POST.get('date').split(' to ')[1]
        else:
            request.session['startdate1']=None
           
      #   print( request.POST.get('loantype'))

        loantyp=request.POST.get('loantype')
        # date= request.POST.get('date')
        if request.POST.get('loantype')!='All':
         request.session['loantype1']=loantyp
         print("Loan time ")
         if request.session.get('All1'):
          del request.session['All1']
        
        else:
            request.session['All1']=loantyp
            if request.session.get('loantype1'):
             del request.session['loantype1']

        request.session['loanstatus']=request.POST.get('loanstatus')
        
        # search By Application Id...........
     if request.POST.get('applicationid1'):
         request.session['applicationid2']=request.POST.get('applicationid1')
         # print(request.POST.get('applicationid1')+ "jjjjkk111")
         if request.session.get('loantype1') or request.session.get('All1'):
          request.session['All1']=None
          request.session['loantype1']=None
     else:
      #  request.session['applicationid2']=None
       if request.session.get('applicationid2'):
          del request.session['applicationid2']
# search By Application Id
      
        
   filterLoans=[] 
   allLoansVariable=[]
   allLoansVariableCopy=0


   # For TO MAKE EXECUTION TIME LESS..
   with ThreadPoolExecutor() as executor:
        future_business = executor.submit(businessLoanApi, request)
        future_education = executor.submit(educationLoanApi, request)

        
   business_result = future_business.result()
   education_result = future_education.result()
      
   if business_result:
            allLoansVariable.extend(business_result)
   if education_result:
            allLoansVariable.extend(education_result)

# OLD APPROACH
   # if businessLoanApi(request):
   #    allLoansVariable.extend(businessLoanApi(request))
   # if educationLoanApi(request):
   #    allLoansVariable.extend(educationLoanApi(request))

   if request.session.get('comission'):
        return allLoansVariable

   AlltotalLoansAmount=0
   if allLoansVariable:
       allLoansVariableCopy=len(allLoansVariable)
       for amount in allLoansVariable:
          AlltotalLoansAmount+=float(amount.get('required_loan_amount'))
          
   # Search Input
   if request.session.get('applicationid2'):
       for loans in allLoansVariable:
          if loans.get('application_id')== request.session.get('applicationid2'):
             filterLoans.append(loans)
      #  print("(0000000000)")

       if not filterLoans:
          request.session['applicationid2']=None
          return render(request,'DataTable.html',{'objects': []})
      #  del request.session['applicationid2']
       allLoansVariable=filterLoans
# Search Input



   if request.session.get('loantype1'):
     print("loantype1")
     print(request.session.get('loanstatus'),"kkkkkkkkkkkk-0")
     if request.session.get('loanstatus')!="All" and request.session.get('loanstatus')!="Pending" and request.session.get('loanstatus')!="Disbursed":
       for loans in allLoansVariable:
      #   loans.get('applicationverification')
     
        if loans.get('verification') is not None:
          a=loans.get('verification')
         #  print("pp1..")
         #  print(a.get('verification_status'))
          if request.session.get('startdate1') and a.get('verification_status')== request.session.get('loanstatus') and loans.get('application_loan_type')==request.session.get('loantype1') and  loans.get('created_at') >= request.session.get('startdate1') and loans.get('created_at') <= request.session.get('enddate1'):
           filterLoans.append(loans)
          if not request.session.get('startdate1') and loans.get('application_loan_type')==request.session.get('loantype1') and a.get('verification_status')== request.session.get('loanstatus'):
         #   print("pp1.0....")
           filterLoans.append(loans)
       allLoansVariable=filterLoans

     elif request.session.get('loanstatus')=="Pending":
       for loans in allLoansVariable:
        if loans.get('verification') is None:
          a=loans.get('verification')
         #  print("pp2..")
         #  print(loans.get('created_at'))
          if  request.session.get('startdate1') and loans.get('application_loan_type')==request.session.get('loantype1') and  loans.get('created_at') >= request.session.get('startdate1') and loans.get('created_at') <= request.session.get('enddate1'):
           filterLoans.append(loans)
          if not request.session.get('startdate1') and loans.get('application_loan_type')==request.session.get('loantype1'):
           filterLoans.append(loans)
       allLoansVariable=filterLoans

     elif request.session.get('loanstatus')=="Disbursed":
        result=[]
        disbursids=disbursedTotalLoanIds(request)
        for i in allLoansVariable:
           for j in disbursids:
              if  request.session.get('startdate1') and i.get('application_id')==j['application_id'] and  loans.get('created_at') >= request.session.get('startdate1') and loans.get('created_at') <= request.session.get('enddate1'):
                 result.append(i)
              if not request.session.get('startdate1') and i.get('application_id')==j['application_id']:
                 result.append(i)
        allLoansVariable=result
           
        
     elif request.session.get('loanstatus')=="All":
        print("All Executed")
        for loans in allLoansVariable:
         #   print("pp3..")
         #   print(loans.get('created_at'))
           if  request.session.get('startdate1') and loans.get('application_loan_type')==request.session.get('loantype1') and  loans.get('created_at') >= request.session.get('startdate1') and loans.get('created_at') <= request.session.get('enddate1'):
            filterLoans.append(loans)
           if not request.session.get('startdate1') and loans.get('application_loan_type')==request.session.get('loantype1'):
            filterLoans.append(loans)
        print(filterLoans)
        allLoansVariable=filterLoans

        if request.session.get('loansteps'):
           uploadFilters=[]
           print("Upload filters",request.session.get('loansteps'))
         #   print("Upload ,,,,,,,//.......")
           if request.session.get('loansteps')=="Uploaddocuments":
              
              for loans in allLoansVariable:
               #   print("Upload Executed.......")
                 if loans.get('documents') is not None:
                  #   print("Upload Executed.......")
                    uploadFilters.append(loans)
              allLoansVariable=uploadFilters
            
           elif request.session.get('loansteps')=="Notuploaddocuments":
              print("NOt Upload Doc")
              for loans in allLoansVariable:
               #   print("Upload Executed.......")
                 if loans.get('documents') is None:
                  #   print("Upload Executed.......")
                    uploadFilters.append(loans)
              allLoansVariable=uploadFilters
      #   print("All status")
    
              


   if request.session.get('All1'):
      print("All executed..........")
      if request.session.get('loanstatus')!="All" and request.session.get('loanstatus')!="Pending" and request.session.get('loanstatus')!="Disbursed":
       for loans in allLoansVariable:
      #   loans.get('applicationverification')
     
         if loans.get('verification') is not None:
           a=loans.get('verification')
         #  print("pp1..")
         #   print(a.get('verification_status'))
           if request.session.get('startdate1') and a.get('verification_status')== request.session.get('loanstatus') and loans.get('created_at') >= request.session.get('startdate1') and loans.get('created_at') <= request.session.get('enddate1'):
            filterLoans.append(loans)
           if not request.session.get('startdate1') and a.get('verification_status')== request.session.get('loanstatus'):
         #   print("pp1.0....")
            filterLoans.append(loans)
       allLoansVariable=filterLoans
      
      elif request.session.get('loanstatus')=="All":
        for loans in allLoansVariable:
         #   print("pp3..")
         #   print(loans.get('created_at'))
           if  request.session.get('startdate1') and  loans.get('created_at') >= request.session.get('startdate1') and loans.get('created_at') <= request.session.get('enddate1'):
            filterLoans.append(loans)
           if not request.session.get('startdate1'):
            filterLoans.append(loans)
        allLoansVariable=filterLoans

        if request.session.get('loansteps'):
           uploadFilters=[]
         #   print("Upload ,,,,,,,//.......")
           if request.session.get('loansteps')=="Uploaddocuments":
              
              for loans in allLoansVariable:
               #   print("Upload Executed.......")
                 if loans.get('documents') is not None:
                  #   print("Upload Executed.......")
                    uploadFilters.append(loans)

              allLoansVariable=uploadFilters
              
           elif request.session.get('loansteps')=="Notuploaddocuments":
              for loans in allLoansVariable:
               #   print("Upload Executed.......")
                 if loans.get('documents') is None:
                  #   print("Upload Executed.......")
                    uploadFilters.append(loans)
              allLoansVariable=uploadFilters

      elif request.session.get('loanstatus')=="Disbursed":
        result=[]
        disbursids=disbursedTotalLoanIds(request)
        for i in allLoansVariable:
           for j in disbursids:
              if i.get('application_id')==j['application_id']:
                 result.append(i)
        allLoansVariable=result

      elif request.session.get('loanstatus')=="Pending":
       for loans in allLoansVariable:
        if loans.get('verification') is None:
          a=loans.get('verification')
         #  print("pp2..")
         #  print(loans.get('created_at'))
          if  request.session.get('startdate1') and  loans.get('created_at') >= request.session.get('startdate1') and loans.get('created_at') <= request.session.get('enddate1'):
           filterLoans.append(loans)
          if not request.session.get('startdate1'):
           filterLoans.append(loans)
       allLoansVariable=filterLoans

    

   if allLoansVariable:
    #  print(allLoans)
     paginator = Paginator(allLoansVariable, 1)  
     page = request.GET.get('page') 
    
     try:
        objects = paginator.page(page)
     except PageNotAnInteger:
        objects = paginator.page(1)
     except EmptyPage:
        objects = paginator.page(1)
        

    
     start_index = (objects.number - 1) * paginator.per_page + 1
   #   print(f"{objects.number}---{paginator.per_page}")

     


     if request.session.get('applicationid2'):
       request.session['applicationid2']=None
      #  print(allLOans)
       return render(request,'DataTable.html',{'objects': objects,'start_index': start_index})

    
   #   findingMaxMinLengthLoans=[]
     approvalLoansLength,rejectedLoansLength,pendingLoans,disbursedLoansLength=0,0,0,0
     approvalLoansAmount,rejectedLoansAmount,pendingLoansAmount,disbursedTotalAmunt=0,0,0,0

     disbursdAmount=disbursedTotalAmount(request)
     if disbursdAmount:
        disbursedTotalAmunt=disbursdAmount
      #   print(disbursedTotalAmunt)
     disbusedLoans=disbursedTotalLoans(request)
     if disbusedLoans:
        disbursedLoansLength=disbusedLoans
      
     request.session['FromalloanstoApproved']=True
     
     approvedLoans(request)
     if request.session.get('approvedLoansLength'):
       approvalLoansLength=request.session.get('approvedLoansLength')
       approvalLoansAmount=request.session.get('approvedLoansAmount')
       del request.session['approvedLoansAmount']
       del request.session['approvedLoansLength']
   
     del request.session['FromalloanstoApproved']
      
       
      #  print("Approved..")
      #  print(request.session.get('approvedLoansLength'))
      #  print(approvalLoansAmount)
     request.session['FromalloanstoRejectd']=True
     
     rejectedLoans(request)
     if request.session.get('rejectedLoansLength'):
       print("If block rejectedLoansLength")
       rejectedLoansLength=request.session.get('rejectedLoansLength')
       rejectedLoansAmount=request.session.get('rejectedLoansAmount')
       del request.session['rejectedLoansLength']
       del request.session['rejectedLoansAmount']
       
     del request.session['FromalloanstoRejectd']
       
      #  print("Rejected..")
      #  print(request.session.get('rejectedLoansLength'))
      #  print(rejectedLoansAmount)
     print("pendingLoans---------------1")
     if allLoansVariableCopy:
       pendingLoans=allLoansVariableCopy-(approvalLoansLength+rejectedLoansLength)
       pendingLoansAmount=AlltotalLoansAmount-(approvalLoansAmount+rejectedLoansAmount)
       print("pendingLoans---------------2")
       print(pendingLoans)
       

      #  print("All loans..")
      #  print(allLoansVariableCopy)
      #  print(AlltotalLoansAmount)

   #   print("pending loans..")
   #   if pendingLoans:
      #  print(pendingLoans)
      #  print(pendingLoansAmount)

    

     loansTitle=['ApprovedLoans','RejectedLoans','Pending Loans','DisbursedLoans']
     numberOfLoans=[approvalLoansLength,rejectedLoansLength,pendingLoans,disbursedLoansLength]

     loansAmountTitle=['ApprovedAmount','RejectedAmount','PendingAmount','DisbursedAmount']
     loansAmounts=[approvalLoansAmount,rejectedLoansAmount,pendingLoansAmount,disbursedTotalAmunt]
     print("REjected Amount............")
     print(rejectedLoansAmount)

     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      #   print("Ajex method is activate..........")
        return render(request, 'DataTable.html', {'objects': objects, 'start_index': start_index})
    
     return render(request, "AllLoansPage.html",{'objects': objects, 'start_index': start_index,'title':"All Loans",'showgraph':True,'loanstitle':loansTitle,'loansCount':numberOfLoans,'totalLoans':allLoansVariableCopy,'loansAmountTitle':loansAmountTitle,'loansAmounts':loansAmounts,'AlltotalLoansAmount':AlltotalLoansAmount,'template':template,'isTrue':an})
   else:
     return render(request, "AllLoansPage.html", {'objects': [],'title':"All Loans",'template':template,'isTrue':an})



def showAllLoansGraph(request):
    a = "jiii"
    return render(request, "AllLoansGraph.html", {'data': a})
 
 
 #All DSA Records Count Logic
 
def business_Loans_Count(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/business_loan_refCode_LoansCount/')
   if response.status_code==200:
      return response.json()
   else: return None
   
def business_Loans_ApprovedCount(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/business_loan_refcode_ApprovedCount/')
   if response.status_code==200:
      return response.json()
   else: return None
   
   
def business_Loans_RejectedCount(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/business_loan_refcode_RejectedCount/')
   if response.status_code==200:
      return response.json()
   else: return None
   
   
def education_Loans_Count(request,refCode):
   
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/el/EduViewsets/{refCode}/education_loan_refCode_LoansCount/')
   if response.status_code==200:
      return response.json()
   else: return None
   
   
def education_Loans_ApprovedCount(request,refCode):
   
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/el/EduViewsets/{refCode}/education_loan_refcode_ApprovedCount/')
   if response.status_code==200:
      return response.json()
   else: return None
   
   
def education_Loans_RejectedCount(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/el/EduViewsets/{refCode}/education_loan_refcode_RejectedCount/')
   if response.status_code==200:
      return response.json()
   else: return None
   
   
   
#Dsa IDS......................................
def getAllDsaIds(request):
   res=requests.get(f'http://127.0.0.1:999/api/mymodel/custom_getOnlyRefCode/')
   if res.status_code==200:
      return res.json()
#Dsa IDS.................................... 
 
 
 
 #All History Data...............................
def totalLoansCount(request):
   dsaIds=getAllDsaIds(request)
   listData=[]
   with ThreadPoolExecutor() as executor:
      for i in dsaIds:
         
      #Demo To find execution time...............
      #   busCount=business_Loans_Count(request,i.get('dsa_registerid'))
      #   busApprCount=business_Loans_ApprovedCount(request,i.get('dsa_registerid'))
      #   busrejectedCount=business_Loans_RejectedCount(request,i.get('dsa_registerid'))
        
        #Business...........................
        businessTotalLoansThread1 = executor.submit(business_Loans_Count, request,i.get('dsa_registerid'))
        businessTotalApprovedThread2=executor.submit(business_Loans_ApprovedCount,request,i.get('dsa_registerid'))
        businessTotalApprovedThread3=executor.submit(business_Loans_RejectedCount,request,i.get('dsa_registerid'))
        
        busCount=businessTotalLoansThread1.result()
        busApprCount=businessTotalApprovedThread2.result()
        busrejectedCount=businessTotalApprovedThread3.result()
        
        #Education...............................
        educationTotalLoansThread1 = executor.submit(education_Loans_Count, request,i.get('dsa_registerid'))
        educationTotalApprovedThread2=executor.submit(education_Loans_ApprovedCount,request,i.get('dsa_registerid'))
        educationTotalApprovedThread3=executor.submit(education_Loans_RejectedCount,request,i.get('dsa_registerid'))
        
        eduCount=educationTotalLoansThread1.result()
        eduApprvdCount=educationTotalApprovedThread2.result()
        eduRejectCount=educationTotalApprovedThread3.result()
        
        
        #Calculation..............................
        totalLoans=busCount.get('count')+eduCount.get('count')
        totalApprvdloans=busApprCount.get('count')+eduApprvdCount.get('count')
        totalRejectdLoans=busrejectedCount.get('count')+eduRejectCount.get('count')
        totalPendingLoans=totalLoans-(totalApprvdloans+totalRejectdLoans)
        
        data={
           'registerId':i.get('dsa_registerid'),
           'totalLoans':totalLoans,
           'approvedloans':totalApprvdloans,
           'rejectedLoans':totalRejectdLoans,
           'pendingLoans':totalPendingLoans
        }
        listData.append(data)
   return JsonResponse(listData,safe=False)
      #   future_education = executor.submit(educationLoanApi, request)

    

    
