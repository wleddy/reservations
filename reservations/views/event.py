from flask import request, session, g, redirect, url_for, \
     render_template, flash, Blueprint
from shotglass2.takeabeltof.date_utils import getDatetimeFromString
from shotglass2.takeabeltof.utils import printException, cleanRecordID
from shotglass2.users.admin import login_required, table_access_required
from reservations.models import Event, Location

from datetime import datetime, date

PRIMARY_TABLE = Event

mod = Blueprint('event',__name__, template_folder='templates/event/', url_prefix='/event')


def setExits():
    g.listURL = url_for('.display')
    g.editURL = url_for('.edit')
    g.deleteURL = url_for('.display') + 'delete/'
    g.title = 'Events'


from shotglass2.takeabeltof.views import TableView

# this handles table list and record delete
@mod.route('/<path:path>',methods=['GET','POST',])
@mod.route('/<path:path>/',methods=['GET','POST',])
@mod.route('/',methods=['GET','POST',])
@table_access_required(PRIMARY_TABLE)
def display(path=None):
    setExits()
    
    view = TableView(PRIMARY_TABLE,g.db)
    # optionally specify the list fields
    # view.list_fields = [
#             {'name':'id','label':'ID','class':'w3-hide-small','search':True},
#             {'name':'description'},
#             {'name':'rank'},
#         ]
    
    return view.dispatch_request()
    

## Edit the PRIMARY_TABLE
@mod.route('/edit', methods=['POST', 'GET'])
@mod.route('/edit/', methods=['POST', 'GET'])
@mod.route('/edit/<int:rec_id>/', methods=['POST','GET'])
@table_access_required(PRIMARY_TABLE)
def edit(rec_id=None):
    setExits()
    g.title = "Edit {} Record".format(g.title)

    # import pdb;pdb.set_trace()
    
    event = PRIMARY_TABLE(g.db)
    rec = None
    locations = Location(g.db).select()
    
    if rec_id == None:
        rec_id = request.form.get('id',request.args.get('id',-1))

    rec_id = cleanRecordID(rec_id)

    if rec_id < 0:
        flash("That is not a valid ID")
        return redirect(g.listURL)

    if rec_id == 0:
        rec = event.new()
    else:
        rec = event.get(rec_id)
        if not rec:
            flash("Unable to locate that record")
            return redirect(g.listURL)

    if request.form:
        event.update(rec,request.form)
        if validForm(rec):
            event.save(rec)
            g.db.commit()

            return redirect(g.listURL)

    # display form
    return render_template('event_edit.html', 
        rec=rec,
        locations=locations,
        )
    
    
def validForm(rec):
    # Validate the form
    goodForm = True
    
    if rec.title and rec.title.strip():
        pass
    else:
        flash("You must give the event a title")
        goodForm = False
        
    if not isinstance(getDatetimeFromString(rec.start),(date,datetime,)):
        flash("That is not a valid Starting Date")
        goodForm = False
                
    if not isinstance(getDatetimeFromString(rec.end),(date,datetime,)):
        flash("That is not a valid Ending Date")
        goodForm = False
        
    if goodForm:
        if rec.end <= rec.start:
            flash("The Starting date must be before the Ending date")
            goodForm = False
        
    return goodForm
    
