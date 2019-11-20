
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

def loginReg(request):
    return render(request, 'main/loginReg.html')

def index(request):
    user = User.objects.all()
    userList = []
    for users in user:
        userList.append(users)
    return render(request, 'main/index.html', context = {'user' : userList})

def processReg(request):
    errors = User.objects.registerValidator(request.POST)  
    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        return redirect('/loginReg')
    else:
        newFirstName = request.POST['firstName']
        newLastName = request.POST['lastName']
        newEmail = request.POST['email']
        newPassword = request.POST['password']
        hashPW = bcrypt.hashpw(newPassword.encode(), bcrypt.gensalt())    
        users = User.objects.filter(email = newEmail)
        if users:
            return redirect('/loginReg')
        else:
            user = User.objects.create(firstName = newFirstName, lastName = newLastName, email = newEmail, password = hashPW)
            request.session['loggedUserID'] = user.id 
            loggedUserID= user.id
            return redirect(f'{loggedUserID}/edit')

def processLogin(request):
    errors = User.objects.loginValidator(request.POST)    
    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        return redirect('/loginReg')
    else:
        user = User.objects.filter(email = request.POST['email']) 
        if user:
            user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['loggedUserID'] = user.id
                loggedUserID = user.id
                return redirect(f'{loggedUserID}/about')
        return redirect("/loginReg")

def about(request, userID):
    if 'loggedUserID' in request.session:
        if int(request.session['loggedUserID']) == int(userID):
            loggedUserID = request.session['loggedUserID']
            loggedUser = User.objects.get(id = loggedUserID)
            page = User.objects.get(id = userID)
            pageID = page.id
            reviews = Review.objects.filter(instructor = page).count()  
            appointments = Appointment.objects.filter(instructor = page).count()  
            return render(request, 'main/about.html', context = {"loggedUser" : loggedUser, "page" : page, "review" : reviews, "appointment" : appointments})
        else:
            page = User.objects.get(id = userID)
            reviews = Review.objects.filter(instructor = page).count()  
            return render(request, 'main/about.html', context = {"page" : page, "review" : reviews})
    else:
        page = User.objects.get(id = userID)
        reviews = Review.objects.filter(instructor = page).count()  
        return render(request, 'main/about.html', context = {"page" : page, "review" : reviews})
    return render(request, 'main/index.html')

def review(request, userID):
    if 'loggedUserID' in request.session:
        if int(request.session['loggedUserID']) == int(userID):
            loggedUserID = request.session['loggedUserID']
            loggedUser = User.objects.get(id = loggedUserID)
            page = User.objects.get(id = userID)
            appointments = Appointment.objects.filter(instructor = page).count()  
            review = Review.objects.filter(instructor = page)
            return render(request, 'main/review.html', context = {"loggedUser" : loggedUser, "page" : page, "review" : review, "reviewCount" :review.count(), "appointments" : appointments })
        else:
            page = User.objects.get(id = userID)
            review = Review.objects.filter(instructor = page)
            return render(request, 'main/review.html', context = {"page" : page, "review" : review, "reviewCount" :review.count()})
    else:
        page = User.objects.get(id = userID)
        review = Review.objects.filter(instructor = page)
        return render(request, 'main/review.html', context = {"page" : page, "review" : review, "reviewCount" :review.count()})
    return redirect(f'/{userID}/about')

def schedule(request, userID):
    if 'loggedUserID' in request.session:
        return redirect(f'/{userID}/about')
    else:
        page = User.objects.get(id = userID)
        review = Review.objects.filter(instructor = page)
        return render(request, 'main/schedule.html', context = {"page" : page, "reviewCount" :review.count()})

def likeReview(request, userID):
    review = Review.objects.get(id = userID)
    review.likes += 1
    review.save()
    page = review.instructor
    pageID = page.id
    return redirect(f'/{pageID}/review')

def addReview(request, userID):
    if 'loggedUserID' in request.session:
        return redirect(f'/{userID}/review')
    else:
        page = User.objects.get(id = userID)
        review = Review.objects.filter(instructor = page)
        return render(request, 'main/addReview.html', context = {"page" : page, "reviewCount" :review.count(),  "appointments" : appointments })

def processReview(request, userID):
    errors = Review.objects.reviewValidator(request.POST)    
    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        print(errors)
        return redirect(f'/{userID}/addReview')
    else:
        name = request.POST['name']
        desc = request.POST['desc']
        recommend = request.POST['recommend']
        bestFeature = request.POST['bestFeature']
        instructor = User.objects.get(id = userID)
        Review.objects.create(name = name, desc = desc, recommend = recommend, bestFeature = bestFeature, likes = 0, instructor = instructor)
        return redirect(f'/{userID}/review')

def edit(request, userID):
    if 'loggedUserID' in request.session:
        if int(request.session['loggedUserID']) == int(userID):
            loggedUserID = request.session['loggedUserID']
            loggedUser = User.objects.get(id = loggedUserID)
            page = User.objects.get(id = loggedUserID)
            appointments = Appointment.objects.filter(instructor = page).count()
            review = Review.objects.filter(instructor = page)
            return render(request, 'main/edit.html', context = {"loggedUser" : loggedUser, "page" : page,  "reviewCount" :review.count(), "appointments" : appointments})
    else:
        return redirect('/index')

def processEdit(request, userID): 
    errors = User.objects.editValidator(request.POST)    
    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        return redirect(f'{userID}/edit')
    newBio = request.POST['bio']
    newExp = request.POST['exp']
    newPrice = request.POST['price']
    newLocation = request.POST['location']
    newSpecialty = request.POST['specialty']
    editProfile = User.objects.get(id = userID)
    editProfile.bio = newBio
    editProfile.price = newPrice
    editProfile.exp = newExp
    editProfile.location = newLocation
    editProfile.specialty = newSpecialty
    editProfile.save()
    profileID = editProfile.id
    return redirect(f'/{profileID}/about')

def processRequest(request, userID):
    errors = Appointment.objects.appointmentValidator(request.POST)    
    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        print(errors)
        return redirect(f'/{userID}/makeAppointment')
    name= request.POST['name']
    email = request.POST['email']
    poolAccess= request.POST['poolAccess']
    availability = request.POST['availability']
    message = request.POST['message']
    lesson = request.POST['lesson']
    instructor = User.objects.get(id = userID)
    Appointment.objects.create(name = name, email = email, poolAccess = poolAccess, message = message, availability = availability, lesson = lesson, instructor = instructor)
    return redirect(f'/{userID}/about')

def appointments(request, userID):
    if 'loggedUserID' in request.session:
        if int(request.session['loggedUserID']) == int(userID):
            loggedUserID = request.session['loggedUserID']
            loggedUser = User.objects.get(id = loggedUserID)
            page = User.objects.get(id = loggedUserID)
            appointment = Appointment.objects.filter(instructor = page)
            appointments = Appointment.objects.filter(instructor = page).count()
            reviews = Review.objects.filter(instructor = page).count()
            return render(request, 'main/appointment.html', context = {"loggedUser" : loggedUser, "page" : page, "appointment" : appointment, "appointments" : appointments, "reviews" : reviews})
        else:
            return redirect(f'/{userID}/about')
    else:
        return redirect(f'/{userID}/about')

def takeAppointment(request, userID):
    appointment = User.objects.get(id = userID)
    appointment.numAppointment += 1
    appointment.save()
    page = appointment.instructor
    pageID = page.id
    return redirect(f'/{pageID}/deleteAppointment')

def deleteAppointment(request, userID):
    appDelete = Appointment.objects.filter(id = userID)
    appDelete.delete()
    return redirect(f'/{userID}/appointments')

def logout(request):
    del request.session['loggedUserID']
    return redirect('/loginReg')

