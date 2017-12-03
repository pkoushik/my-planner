import string

from app.modules.auth.model import User
from app.modules.events.model import Event, EventCreateForm
from app.modules.classes.model import Meeting, MeetingCreateForm, MeetingUpdateForm, MeetingDeleteForm
from flask import Blueprint, request, render_template, flash, redirect, \
    url_for, jsonify
from flask_security import login_required, current_user


events = Blueprint('events', __name__)





def filter_form(form):
    """ Router for CRUD Forms that were Recieved on the event Dashboard """

    if form['submit'] == 'create':
        return create_event(form)
    elif form['submit'] == 'update':
        return update_event(form)
    elif form['submit'] == 'delete':
        return delete_event(form)

    flash('error Could not Fulfill Request. Please Try Again.')
    return redirect(url_for('classes.home'))


def event_filter_form(form):
    """ Router for CRUD Forms Recevied in the event Landing Page """

    if form['submit'] == 'create':
        return create_event_meeting(form)
    elif form['submit'] == 'update':
        return update_event_meeting(form)
    elif form['submit'] == 'delete':
        return delete_event_meeting(form)

    flash('error Could not fullfill request. Please try again')
    return redirect(url_form('events.home'))


#abhis shit
@events.route('/create', methods=['POST'])
@login_required
# def create_event(form=None):
#     if form is None: # there was not a form?
#         create_form = eventCreateForm(request.form)
#     else: # there is a form?
#         create_form = eventCreateForm(form)
	if form is None:
		flash('There was no form idk what to do now')
		return redirect(request.args.get('next') or url_for('events.home'))

    create_form = EventCreateForm(form) # the form for creating a new event

    if not create_form.validate():
        flash('error Could not Create New event, Please Try Again.')
        return redirect(request.args.get('next') or url_for('events.home'))

    try:
        user = current_user._get_current_object() # get the current user

        current_event = Event(name=create_form.name.data,typeOfEvent=create_form.typeOfEvent.data, time=create_form.time.data, event_class = create_form.event_class.data)

        user.events.append(current_event)



    except Exception as e:
        flash('An error has happened, oh noes '
              '{}'.format(str(e)))

    return redirect(request.args.get('next') or url_for('events.home'))
        



# no longer abhis shit


# @events.route('/delete-meeting', methods=['POST'])
# @login_required
# def delete_event_meeting(form=None):
#     """ Delete and existing event meeting """

#     if form is None:
#         flash('error Invalid Request to delete meeting.')
#         return redirect(request.args.get('next') or url_for('events.home'))

#     delete_form = MeetingDeleteForm(form)

#     if not delete_form.validate():
#         flash('error You do not have permission to delete this meeting.')
#         return redirect(url_form('events.home'))

#     try:
#         user = current_user._get_current_object()
#         meeting = Meeting.objects.get(id=delete_form.meeting_id.data)
#         events = event.objects(classes__contains=meeting)

#         members = meeting.members
#         owner = meeting.owner

#         # user is not the owner of event and cannot delete
#         if user != owner:
#             flash('error You do not have permission to delete this meeting.')
#             return redirect(url_for('events.home'))

#         # remove the meeting from each member's list of meeting
#         for member in members:
#             if meeting in member.classes:
#                 member.classes.remove(meeting)
#                 member.meeting_count = member.meeting_count - 1
#                 member.save()

#         # remove meeting from owner's list of classes
#         if meeting in owner.classes:
#             owner.classes.remove(meeting)
#             owner.meeting_count = member.meeting_count - 1
#             owner.save()

#         # remove meeting from owner's list of events
#         for event in user.events:
#             if meeting in event.classes:
#                 event.classes.remove(meeting)
#                 event.save()
#         meeting.delete()
#         flash('success Meeting successfully deleted')

#     except Exception as e:
#         flash('error An error has occured, please try again {}'.format(str(e)))
#     return redirect(request.args.get('next') or url_for('events.home'))


# @events.route('/update-meeting', methods=['POST'])
# @login_required
# def update_event_meeting(form=None):
#     """ Update and existing meeting from the event landing page"""
#     if form is None:
#         flash("error Invalid Request to update meeting")
#         return redirect(request.args.get('next') or url_for('events.home'))
#     update_form = MeetingUpdateForm(form)

#     if not update_form.validate():
#         flash("error Could not update meeting, please try again")
#         return redirect(request.args.get('next') or url_for('events.home'))
#     try:
#         # extract form data
#         name = update_form.name.data
#         emails_to_add_str = update_form.emails_to_add.data
#         emails_to_remove_str = update_form.emails_to_remove.data

#         # search for the meeting
#         meeting = Meeting.objects.get(id=update_form.meeting_id.data)

#         members = meeting.members

#         # remove the undesired members
#         if len(emails_to_remove_str) != 0:
#             emails_to_remove = emails_to_remove_str.split("")
#             members_to_remove = User.objects(email__in=emails_to_remove)

#             # remove the meeting from each members list of classes
#             for member in members_to_remove:
#                 if meeting in member.classes:
#                     member.meeting_count = member.meeting_count - 1
#                     member.classes.remove(meeting)
#                     member.save()
#             # remove members from the list
#             members = list(filter(
#                 lambda x: x not in members_to_remove, members))

#         # add new members
#         if len(emails_to_add_str) != 0:
#             emails_to_add = emails_to_add_str.split(" ")
#             members_to_add = User.objects(email__in=emails_to_add)

#             for member in members_to_add:
#                 # add member to the meeting's list of members
#                 if member not in members:
#                     members.append(member)

#                 # add meeting to the member's list of classes
#                 if meeting not in member.classes:
#                     member.classes.append(meeting)
#                     member.save()

#         # save all the changes
#         meeting.name = name
#         meeting.members = members
#         meeting.save()

#         flash('success Meeting has been successfully updated.')
#     except Exception as e:
#         flash("error An error has occcured, please try again: {}".format(e))

#     return redirect(url_for('events.home'))


# @events.route('/create-meeting', methods=['POST'])
# @login_required
# def create_event_meeting(form=None):
#     """ Creates a new meeting from the event landing page """
#     if form is None:
#         flash("error Invalid Request to create meeting")
#         return redirect(request.args.get('next') or url_for('events.home'))
#     create_form = MeetingCreateForm(form)

#     if not create_form.validate():
#         flash("error Could not create new meeting, please try again")
#         return redirect(request.args.get('next') or url_for('events.home'))
#     try:
#         user = current_user._get_current_object()

#         emails = create_form.emails.data.split(" ")
#         emails.append(user.email)

#         # generate list of valid emails - should be valid unless a user is deleted
#         query = User.objects(email__in=emails)
#         valid_emails = [u.email for u in query]

#         # check if emails are complete, if not, display incorrect and cancel request
#         if len(valid_emails) != len(emails):
#             invalid_emails = list(set(emails) - set(valid_emails))
#             flash("error We were unable to find user(s): {}".format(invalid_emails))
#             return redirect(url_for('events.home'))
#         # validate and create meeting
#         m = Meeting(name=create_form.name.data,
#                     members=query,
#                     owner=user,
#                     meeting_nature=create_form.nature.data,
#                     active=False).save()
#         # insert meeting into each user's list of classes
#         for u in query:
#             u.classes.append(m)
#             u.meeting_count = u.meeting_count + 1
#             u.save()

#         # insert meeting into this event
#         # query to find event associated
#         g = event.objects.get(members=query)
#         g.classes.append(m)
#         g.save()

#         flash("success Meeting successfully created with event {}".format(g.name))
#         return redirect(url_for('events.get_event_by_id', event_id=g.id))
#     except Exception as e:
#         flash("error An error has occcured, please try again: {}".format(e))
#     return redirect(url_for('events.home'))


# @events.route('/', methods=['GET', 'POST'])
# @login_required
# def home():
#     """ Displays All of the Current User's events on the event Dashboard """
#     if request.method == 'POST':
#         return filter_form(request.form)

#     user = current_user._get_current_object()
#     return render_template('event/dashboard.html', events=user.events)




# @events.route('/create', methods=['POST'])
# @login_required
# def create_event(form=None):
#     """ Creates a new event. """

#     if form is None:
#         create_form = eventCreateForm(request.form)
#     else:
#         create_form = eventCreateForm(form)

#     if not create_form.validate():
#         flash('error Could not Create New event, Please Try Again.')
#         return redirect(request.args.get('next') or url_for('events.home'))

#     try:
#         user = current_user._get_current_object()

#         # generate the list of requested member emails
#         emails = create_form.emails.data.split(" ")
#         emails.append(user.email)

#         # generate the list of valid emails
#         query = User.objects(email__in=emails)
#         valid_emails = [u.email for u in query]

#         # validate and create the new event
#         if len(emails) == len(valid_emails):

#             g = event(name=create_form.name.data, members=query,
#                       admins=[user]).save()

#             # add the event to each member's list of events
#             for u in query():
#                 u.events.append(g)
#                 u.save()

#             flash('success New event Created with Member(s): {}'.format(
#                 ", ".join(valid_emails)))
#             return redirect(request.args.get('next') or url_for('events.home'))
#         else:
#             # determine the invalid emails
#             invalid_emails = list(set(emails) - set(valid_emails))
#             flash('error Could not Create New event. Unable to Find User(s):'
#                   '{}'.format(invalid_emails))
#     except Exception as e:
#         flash('error An Error has Occured, Please Try Again. '
#               '{}'.format(str(e)))

#     return redirect(request.args.get('next') or url_for('events.home'))


# @events.route('/update', methods=['POST'])
# @login_required
# def update_event(form=None):
#     """ Updates an Existing event """

#     if form is None:
#         update_form = eventUpdateForm(request.form)
#     else:
#         update_form = eventUpdateForm(form)

#     if not update_form.validate():
#         flash('error Could Not Update event, Please Try Again.')
#         return redirect(request.args.get('next') or url_for('events.home'))
#     try:
#         # extract the form data
#         name = update_form.name.data
#         description = update_form.description.data
#         emails_to_add_str = update_form.emails_to_add.data
#         admin_emails_to_add_str = update_form.admin_emails_to_add.data
#         emails_to_remove_str = update_form.emails_to_remove.data

#         event = event.objects.get(id=update_form.event_id.data)

#         members = event.members
#         admins = event.admins

#         # remove the undesired members
#         if len(emails_to_remove_str) != 0:
#             emails_to_remove = emails_to_remove_str.split(" ")
#             members_to_remove = User.objects(
#                 email__in=emails_to_remove)

#             # remove the event from each members list of events
#             for member in members_to_remove:
#                 if event in member.events:
#                     member.events.remove(event)
#                     member.save()

#             # remove the members from the list
#             members = list(filter(
#                 lambda x: x not in members_to_remove, members))

#         # add the new members
#         if len(emails_to_add_str) != 0:
#             emails_to_add = emails_to_add_str.split(" ")
#             members_to_add = User.objects(email__in=emails_to_add)

#             for member in members_to_add:
#                 # add member to the event's list of members
#                 if member not in members:
#                     members.append(member)

#                 # add event to the member's list of events
#                 if event not in member.events:
#                     member.events.append(event)
#                     member.save()

#         # add the new admins
#         if len(admin_emails_to_add_str) != 0:
#             admin_emails_to_add = admin_emails_to_add_str.split(" ")
#             admins_to_add = User.objects(
#                 email__in=admin_emails_to_add)

#             for admin in admins_to_add:
#                 # add admin to the event's list of admins
#                 if admin not in admins:
#                     admins.append(admin)

#                 # add admin to the event's list of members
#                 if admin not in members:
#                     members.append(admin)

#                 # add event to the admin's list of events
#                 if event not in admin.events:
#                     admin.events.append(event)
#                     admin.save()

#         # update the description
#         if len(description) != 0:
#             event.description = description

#         # save the changes
#         event.name = name
#         event.members = members
#         event.admins = admins
#         event.save()

#         flash('success event Successfully Updated')

#     except Exception as e:
#         flash('error Unable to Update event at this Time, Please Try Again.'
#               '{}'.format(str(e)))
#         print(str(e))

#     return redirect(request.args.get('next') or url_for('events.home'))


# @events.route('/delete', methods=['POST'])
# @login_required
# def delete_event(form=None):
#     """ Deletes an Existing event """

#     if form is None:
#         flash('error Invalid Request to Delete event.')
#         return redirect(request.args.get('next') or url_for('events.home'))

#     delete_form = eventDeleteForm(form)

#     if not delete_form.validate():
#         flash('error Could not Delete event, Please Try Again.')
#         return redirect(request.args.get('next') or url_for('events.home'))

#     try:
#         user = current_user._get_current_object()
#         event = event.objects.get(id=delete_form.event_id.data)

#         members = event.members
#         admins = event.admins
#         classes = event.classes
#         # validate that the user is an admin for the event
#         if user not in admins:
#             flash('error You do not have permission to delete this event.')
#             return redirect(request.args.get('next') or
#                             url_for('events.home'))

#         # remove the event from each member's list of events
#         for member in members:
#             if event in member.events:
#                 member.events.remove(event)
#                 member.save()

#         # remove the event from each admin's list of events
#         for admin in admins:
#             if event in admin.events:
#                 admin.events.remove(event)
#                 admin.save()

#         # delete all classes associated with event
#         for meeting in classes:
#             # remove meeting from all member's list of classes
#             for member in members:
#                 member.classes.remove(meeting)
#                 member.save()

#             # remove meeting from each admin's list of classes
#             for admin in admins:
#                 admin.classes.remove(meeting)
#                 admin.save()

#             # now delete the entire meeting from the database
#             meeting.delete()
#         event.delete()

#         flash('success event Successfully Deleted')
#     except Exception as e:
#         flash('error An Error has Occured, Please Try Again.'
#               '{}'.format(str(e)))

#     return redirect(request.args.get('next') or url_for('events.home'))


# @events.route('/search=<string:query>', methods=['GET', 'POST'])
# @login_required
# def search_events(query):
#     """ Displays the events that match the query on the event Dashboard """

#     if request.method == 'POST':
#         return filter_form(request.form)

#     events = current_user._get_current_object().events
#     search = query.split(" ")

#     # search is too expensive
#     if len(search) > 20:
#         flash('error Could not Fulfill Search Request.')
#         return redirect(request.args.get('next') or url_for('events.home'))

#     # get the list of users to search for
#     users = list(filter(lambda x: "@" in x, search))

#     # get the other search criteria
#     search = list(filter(lambda x: "@" not in x, search))

#     # filter the events by user
#     for u in users:
#         try:
#             user = User.objects.get(email=u[1:])
#             events = list(filter(lambda x: user in x.members, events))
#         except Exception as e:
#             return render_template('event/dashboard.html', events=[])

#     # filter the classes by name
#     for c in search:
#         events = list(filter(lambda x: c.lower() in x.name.lower(), events))

#     # reset the page and only show the matched events
#     return render_template('event/dashboard.html', events=events)


# @events.route('/<event_id>', methods=['GET', 'POST'])
# @login_required
# def get_event_by_id(event_id, form=None):
#     if request.method == 'POST':
#         return event_filter_form(request.form)

#     # validate the given id
#     if len(event_id) != 24 or not all(c in string.hexdigits for c in event_id):
#         flash('error Invalid event ID')
#         return redirect(request.args.get('next') or url_for('events.home'))

#     try:
#         user = current_user._get_current_object()
#         event = event.objects.get(id=event_id)
#         if user not in event.members:
#             flash('error You Are Not A Member Of This event.')
#             return redirect(request.args.get('next') or url_for('events.home'))

#         emails = []
#         for u in event.members:
#             if u.email != user.email:
#                 emails.append(u.email)
#         emails = " ".join(emails)
#         form = MeetingCreateForm()
#         return render_template('event/event.html', event=event, stats=event_stats(event_id), emails=emails, form=form)

#     except Exception as e:
#         flash('error An Error Occured. {}'.format(str(e)))
#         return redirect(request.args.get('next') or url_for('events.home'))


# @login_required
# def event_stats(event_id):
#     if len(event_id) != 24 or not all(c in string.hexdigits for c in event_id):
#         flash('error Invalid event ID')
#         return redirect(request.args.get('next') or url_for('events.home'))

#     response = dict()

#     try:
#         user = current_user._get_current_object()
#         events = current_user._get_current_object().events
#         event = event.objects.get(id=event_id)

#         if user not in event.members:
#             return {'status': 'invalid permission'}

#         contributions = event.get_member_contributions()
#         sorted_contributors = sorted(contributions, key=contributions.get, reverse=True)
#         sorted_contributors = sorted_contributors[:3]
#         del(sorted_contributors[3:])

#         tags = event.get_frequent_tags()
#         sorted_tags = sorted(tags, key=tags.get, reverse=True)
#         del(sorted_tags[3:])

#         topics = event.get_frequent_topics()
#         sorted_topics = sorted(topics, key=topics.get, reverse=True)
#         del(sorted_topics[3:])

#         # response['contribution'] = event.update_contr()
#         response['contributors'] = sorted_contributors
#         response['tags'] = sorted_tags
#         response['topics'] = sorted_topics

#         return response
#     except Exception as e:
#         response['error'] = str(e)

#     response['status'] = 'failure'
#     return response
