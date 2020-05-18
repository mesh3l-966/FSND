#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import babel
from datetime import date, datetime, time
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate (app,db)
# TODO: connect to a local postgresql database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:laug999@localhost:5432/fyyurdb'
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', backref='venue', lazy=True)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', backref='artist', lazy=True)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'show'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
  

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
#@app.template_filter()
def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  print(date)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')
  #return date.strftime("%b %d %Y %H:%M:%S")

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  venues = Venue.query.all()
  city_states = {(venue.city, venue.state) for venue in venues}
  data = [{'city': cs[0], 'state': cs[1], 'venues': []} for cs in city_states]
  #alternative command:
  #city_states = Venue.query.distinct('city','state').all()
  #data = [{'city': cs.city, 'state': cs.state, 'venues': []} for cs in city_states]

  
  
  for d in data:
    vens = Venue.query.filter_by(city=d['city'], state=d['state']).all()
    d['venues'] = Venue.query.filter_by(city=d['city'], state=d['state']).all()
    #venue_shows = [len(venue.shows) for venue in d['venues']]
    for v in d['venues']:
      num_upcoming_shows = len([show for show in v.shows if show.start_time >= datetime.today()])
      #shows_num = len(v.shows)
      v = v.__dict__
      v['num_upcoming_shows'] = num_upcoming_shows
    #d['venues']['num_upcoming_shows'] = sum(venue_shows)


  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term')
  res = Venue.query.filter(Venue.name.ilike('%'+search_term+'%')).all()
  response = {
    "count":len(res),
    'data':[]
  }
  for venue in res:
    num_upcoming_shows = len([show for show in venue.shows if show.start_time >= datetime.today()])
    ven = {'id':venue.id, 'name':venue.name, 'num_upcoming_shows':num_upcoming_shows}
    response['data'].append(ven)
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  shows = venue.shows
  upcoming_shows = [show for show in shows if show.start_time >= datetime.today()]
  past_shows = [show for show in shows if show.start_time < datetime.today()]
  #shows = [show for show in venue.shows if show.start_time >= datetime.today()]
  data = {
      "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows":     [{'artist_id':show.artist_id, 'artist_name':show.artist.name, 'artist_image_link':show.artist.image_link, 'start_time':str(show.start_time)} for show in past_shows],
    'upcoming_shows': [{'artist_id':show.artist_id, 'artist_name':show.artist.name, 'artist_image_link':show.artist.image_link, 'start_time':str(show.start_time)} for show in upcoming_shows],
    'past_shows_count': len(past_shows),
    'upcoming_shows_count': len(upcoming_shows),
  }
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  address = request.form['address']
  phone = request.form['phone']
  image_link = request.form['image_link']
  genres = request.form.getlist('genres')
  facebook_link = request.form['facebook_link']

  try:
    venue = Venue(name=name, city=city, state=state, address=address, phone=phone, image_link=image_link, genres=genres, facebook_link=facebook_link)
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term')
  res = Artist.query.filter(Artist.name.ilike('%'+search_term+'%')).all()
  response = {
    "count":len(res),
    'data':[]
  }
  for artist in res:
    art = {'id':artist.id, 'name':artist.name}
    response['data'].append(art)
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.get(artist_id)
  shows = artist.shows
  upcoming_shows = [show for show in shows if show.start_time >= datetime.today()]
  past_shows = [show for show in shows if show.start_time < datetime.today()]
  data = {
      "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows":     [{'artist_id':show.artist_id, 'artist_name':show.artist.name, 'artist_image_link':show.artist.image_link, 'start_time':str(show.start_time)} for show in past_shows],
    'upcoming_shows': [{'artist_id':show.artist_id, 'artist_name':show.artist.name, 'artist_image_link':show.artist.image_link, 'start_time':str(show.start_time)} for show in upcoming_shows],
    'past_shows_count': len(past_shows),
    'upcoming_shows_count': len(upcoming_shows),
  }
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  art = Artist.query.get(artist_id)
  form.name.data = art.name
  form.city.data = art.city
  form.state.data = art.state
  form.genres.data = art.genres
  form.phone.data = art.phone
  form.image_link.data = art.image_link
  form.facebook_link.data = art.facebook_link
  artist = {
    "id": art.id, 
    "name": art.name,
    "genres": art.genres,
    "city": art.city,
    "state": art.state,
    "phone": art.phone,
    "website": art.website,
    "facebook_link": art.facebook_link,
    "seeking_venue": art.seeking_venue,
    "seeking_description": art.seeking_description,
    "image_link": art.image_link,
  }
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  image_link = request.form['image_link']
  genres = request.form.getlist('genres')
  facebook_link = request.form['facebook_link']

  try:
    #artist = Artist(name=name, city=city, state=state, phone=phone, image_link=image_link, genres=genres, facebook_link=facebook_link)
    artist.name=name
    artist.city=city
    artist.state=state
    artist.phone=phone
    artist.image_link=image_link
    artist.genres=genres
    artist.facebook_link=facebook_link
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully Edited!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be Edited.')
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  ven = Venue.query.get(venue_id)
  form.name.data = ven.name
  form.city.data = ven.city
  form.state.data = ven.state
  form.genres.data = ven.genres
  form.address.data = ven.address
  form.phone.data = ven.phone
  form.image_link.data = ven.image_link
  form.facebook_link.data = ven.facebook_link

  venue = {
    "id": ven.id, 
    "name": ven.name,
    "genres": ven.genres,
    'address': ven.address,
    "city": ven.city,
    "state": ven.state,
    "phone": ven.phone,
    "website": ven.website,
    "facebook_link": ven.facebook_link,
    "seeking_talent": ven.seeking_talent,
    "seeking_description": ven.seeking_description,
    "image_link": ven.image_link,
  }
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  
  venue = Venue.query.get(venue_id)
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  address = request.form['address']
  phone = request.form['phone']
  image_link = request.form['image_link']
  genres = request.form.getlist('genres')
  facebook_link = request.form['facebook_link']

  try:
    #artist = Artist(name=name, city=city, state=state, phone=phone, image_link=image_link, genres=genres, facebook_link=facebook_link)
    venue.name=name
    venue.city=city
    venue.state=state
    venue.address=address
    venue.phone=phone
    venue.image_link=image_link
    venue.genres=genres
    venue.facebook_link=facebook_link
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully Edited!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be Edited.')
  finally:
    db.session.close()
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  image_link = request.form['image_link']
  genres = request.form.getlist('genres')
  facebook_link = request.form['facebook_link']

  try:
    artist = Artist(name=name, city=city, state=state, phone=phone, image_link=image_link, genres=genres, facebook_link=facebook_link)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  show = {}
  data = []
  shows = Show.query.all()
  for s in shows:
    show = {}
    show['venue_id'] = s.venue.id
    show['venue_name'] = s.venue.name
    show['artist_id'] = s.artist.id
    show['artist_name'] = s.artist.name
    show['artist_image_link'] = s.artist.image_link
    show['start_time'] = str(s.start_time)
    data.append(show)
    
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  artist_id = request.form['artist_id']
  venue_id = request.form['venue_id']
  start_time = request.form['start_time']
  try:
    show = Show(artist_id=artist_id, venue_id=venue_id, start_time= start_time)
    db.session.add(show)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
