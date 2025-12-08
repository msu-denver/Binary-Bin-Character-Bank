from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Character

main = Blueprint('main', __name__)

# ------------------ Registration Helper ------------------

def register_user(username, password):
    """Register a new user and return a message and success flag."""
    if not username or not password:
        return "Missing data", False

    if User.query.filter_by(username=username).first():
        return "Username already taken", False

    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return "User registered", True

# Ability modifiers
CLASS_MODIFIERS = {
    "Fighter": {"strength": 2, "constitution": 1},
    "Rogue": {"dexterity": 2, "intelligence": 1},
    "Wizard": {"intelligence": 2, "wisdom": 1},
}

BACKGROUND_MODIFIERS = {
    "Noble": {"charisma": 1, "intelligence": 1},
    "Soldier": {"strength": 1, "constitution": 1},
    "Sage": {"intelligence": 2},
}

# ------------------ Routes ------------------

@main.route('/')
def index():
    # Landing page with navigation to login or register
    return render_template('index.html')


# ------------------ Authentication ------------------

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid username or password")
    return render_template('login.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash("Username already exists")
        else:
            hashed_password = generate_password_hash(password)
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Registered successfully! Please login.")
            return redirect(url_for('main.login'))
    return render_template('register.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# ------------------ Dashboard ------------------

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# ------------------ Character Creation ------------------

@main.route('/create_character', methods=['GET', 'POST'])
@login_required
def create_character():
    if request.method == 'POST':
        name = request.form['name']
        character_class = request.form['class']
        race = request.form['race']
        background = request.form['background']
        backstory = request.form['backstory']
        is_public = 'public' in request.form

        # -------------------------------
        # Base ability scores by class
        # This overrides the 10-point default
        # -------------------------------
        CLASS_BASES = {
            "Barbarian": {"strength": 15, "dexterity": 13, "constitution": 14,
                        "intelligence": 8, "wisdom": 10, "charisma": 12},
            "Bard": {"strength": 10, "dexterity": 12, "constitution": 14,
                        "intelligence": 8, "wisdom": 13, "charisma": 15},
            "Cleric": {"strength": 12, "dexterity": 13, "constitution": 14,
                        "intelligence": 10, "wisdom": 15, "charisma": 8},
            "Druid": {"strength": 8, "dexterity": 13, "constitution": 10,
                        "intelligence": 12, "wisdom": 15, "charisma": 14},
            "Fighter": {"strength": 15, "dexterity": 14, "constitution": 13,
                      "intelligence": 10, "wisdom": 12, "charisma": 8},
            "Monk": {"strength": 8, "dexterity": 14, "constitution": 13,
                       "intelligence": 10, "wisdom": 15, "charisma": 12},
            "Paladin": {"strength": 15, "dexterity": 10, "constitution": 12,
                        "intelligence": 8, "wisdom": 13, "charisma": 14},
            "Ranger": {"strength": 12, "dexterity": 15, "constitution": 10,
                        "intelligence": 8, "wisdom": 14, "charisma": 13},
            "Rogue": {"strength": 8, "dexterity": 15, "constitution": 13,
                        "intelligence": 10, "wisdom": 12, "charisma": 14},
            "Sorcerer": {"strength": 8, "dexterity": 12, "constitution": 14,
                        "intelligence": 10, "wisdom": 13, "charisma": 15},
            "Warlock": {"strength": 8, "dexterity": 12, "constitution": 10,
                      "intelligence": 13, "wisdom": 14, "charisma": 15},
            "Wizard": {"strength": 8, "dexterity": 12, "constitution": 10,
                       "intelligence": 15, "wisdom": 14, "charisma": 13},
        }

        # -------------------------------
        # Background modifiers to add on top
        # -------------------------------
        BACKGROUND_MODIFIERS = {
            "Acolyte": {"charisma": 1, "intelligence": 1, "wisdom": 1},
            "Artisan": {"strength": 1, "dexterity": 1, "intelligence": 1},
            "Charlatan": {"constitution": 1, "dexterity": 1, "charisma": 1},
            "Criminal": {"constitution": 1, "dexterity": 1, "intelligence": 1},
            "Entertainer": {"strength": 1, "dexterity": 1, "charisma": 1},
            "Farmer": {"strength": 1, "constitution": 1, "wisdom": 1},
            "Guard": {"strength": 1, "intelligence": 1, "wisdom": 1},
            "Guide": {"constitution": 1, "dexterity": 1, "wisdom": 1},
            "Hermit": {"constitution": 1, "wisdom": 1, "charisma": 1},
            "Merchant": {"constitution": 1, "charisma": 1, "intelligence": 1},
            "Noble": {"strength": 1, "charisma": 1, "intelligence": 1},
            "Sage": {"constitution": 1, "wisdom": 1, "intelligence": 1},
            "Sailor": {"strength": 1, "dexterity": 1, "wisdom": 1},
            "Scribe": {"wisdom": 1, "dexterity": 1, "intelligence": 1},
            "Soldier": {"strength": 1, "dexterity": 1, "consitution": 1},
            "Wayfarer": {"wisdom": 1, "dexterity": 1, "charisma": 1},
            }

        # Start with class base scores
        abilities = CLASS_BASES.get(character_class, {
            "strength": 10, "dexterity": 10, "constitution": 10,
            "intelligence": 10, "wisdom": 10, "charisma": 10
        })

        # Apply background modifiers
        for key, value in BACKGROUND_MODIFIERS.get(background, {}).items():
            abilities[key] += value

        # Create character
        character = Character(
            name=name,
            character_class=character_class,
            race=race,
            background=background,
            backstory=backstory,
            is_public=is_public,
            strength=abilities['strength'],
            dexterity=abilities['dexterity'],
            constitution=abilities['constitution'],
            intelligence=abilities['intelligence'],
            wisdom=abilities['wisdom'],
            charisma=abilities['charisma'],
            owner=current_user
        )
        db.session.add(character)
        db.session.commit()
        flash("Character created!")
        return redirect(url_for('main.dashboard'))

    return render_template('create_character.html')

@main.route('/delete_character/<int:character_id>', methods=["POST"])
@login_required
def delete_character(character_id):
    character = Character.query.get_or_404(character_id)

    # Only allow deleting own characters
    if character.owner_id != current_user.id:
        flash("You are not allowed to delete this character.", "error")
        return redirect(url_for('main.my_characters'))

    db.session.delete(character)
    db.session.commit()
    
    flash(f"Character '{character.name}' has been deleted.", "success")
    return redirect(url_for('main.my_characters'))

@main.route('/edit_character/<int:character_id>', methods=['GET', 'POST'])
@login_required
def edit_character(character_id):
    character = Character.query.get_or_404(character_id)

    # Security: prevent editing other users' characters
    if character.owner != current_user:
        flash("You do not have permission to edit this character.")
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        character_class = request.form['class']
        race = request.form['race']
        background = request.form['background']
        backstory = request.form['backstory']
        is_public = 'public' in request.form

        # Detect whether class/background changed
        class_changed = character.character_class != character_class
        background_changed = character.background != background

        # If either changed, recalculate stats
        if class_changed or background_changed:

            CLASS_BASES = {
                "Barbarian": {"strength": 15, "dexterity": 13, "constitution": 14,
                              "intelligence": 8, "wisdom": 10, "charisma": 12},
                "Bard": {"strength": 10, "dexterity": 12, "constitution": 14,
                         "intelligence": 8, "wisdom": 13, "charisma": 15},
                "Cleric": {"strength": 12, "dexterity": 13, "constitution": 14,
                           "intelligence": 10, "wisdom": 15, "charisma": 8},
                "Druid": {"strength": 8, "dexterity": 13, "constitution": 10,
                          "intelligence": 12, "wisdom": 15, "charisma": 14},
                "Fighter": {"strength": 15, "dexterity": 14, "constitution": 13,
                            "intelligence": 10, "wisdom": 12, "charisma": 8},
                "Monk": {"strength": 8, "dexterity": 14, "constitution": 13,
                         "intelligence": 10, "wisdom": 15, "charisma": 12},
                "Paladin": {"strength": 15, "dexterity": 10, "constitution": 12,
                            "intelligence": 8, "wisdom": 13, "charisma": 14},
                "Ranger": {"strength": 12, "dexterity": 15, "constitution": 10,
                           "intelligence": 8, "wisdom": 14, "charisma": 13},
                "Rogue": {"strength": 8, "dexterity": 15, "constitution": 13,
                          "intelligence": 10, "wisdom": 12, "charisma": 14},
                "Sorcerer": {"strength": 8, "dexterity": 12, "constitution": 14,
                             "intelligence": 10, "wisdom": 13, "charisma": 15},
                "Warlock": {"strength": 8, "dexterity": 12, "constitution": 10,
                            "intelligence": 13, "wisdom": 14, "charisma": 15},
                "Wizard": {"strength": 8, "dexterity": 12, "constitution": 10,
                           "intelligence": 15, "wisdom": 14, "charisma": 13},
            }

            BACKGROUND_MODIFIERS = {
                "Acolyte": {"charisma": 1, "intelligence": 1, "wisdom": 1},
                "Artisan": {"strength": 1, "dexterity": 1, "intelligence": 1},
                "Charlatan": {"constitution": 1, "dexterity": 1, "charisma": 1},
                "Criminal": {"constitution": 1, "dexterity": 1, "intelligence": 1},
                "Entertainer": {"strength": 1, "dexterity": 1, "charisma": 1},
                "Farmer": {"strength": 1, "constitution": 1, "wisdom": 1},
                "Guard": {"strength": 1, "intelligence": 1, "wisdom": 1},
                "Guide": {"constitution": 1, "dexterity": 1, "wisdom": 1},
                "Hermit": {"constitution": 1, "wisdom": 1, "charisma": 1},
                "Merchant": {"constitution": 1, "charisma": 1, "intelligence": 1},
                "Noble": {"strength": 1, "charisma": 1, "intelligence": 1},
                "Sage": {"constitution": 1, "wisdom": 1, "intelligence": 1},
                "Sailor": {"strength": 1, "dexterity": 1, "wisdom": 1},
                "Scribe": {"wisdom": 1, "dexterity": 1, "intelligence": 1},
                "Soldier": {"strength": 1, "dexterity": 1, "constitution": 1},
                "Wayfarer": {"wisdom": 1, "dexterity": 1, "charisma": 1},
            }

            # Recalculate stats
            abilities = CLASS_BASES.get(character_class, {
                "strength": 10, "dexterity": 10, "constitution": 10,
                "intelligence": 10, "wisdom": 10, "charisma": 10
            })

            for key, value in BACKGROUND_MODIFIERS.get(background, {}).items():
                abilities[key] += value

            character.strength = abilities['strength']
            character.dexterity = abilities['dexterity']
            character.constitution = abilities['constitution']
            character.intelligence = abilities['intelligence']
            character.wisdom = abilities['wisdom']
            character.charisma = abilities['charisma']

        # Update text fields always
        character.name = name
        character.character_class = character_class
        character.race = race
        character.background = background
        character.backstory = backstory
        character.is_public = is_public

        db.session.commit()
        flash("Character updated!")
        return redirect(url_for('main.dashboard'))

    return render_template('create_character.html', character=character, edit=True)


@main.route('/copy_character/<int:char_id>', methods=['POST'])
@login_required
def copy_character(char_id):
    original = Character.query.get_or_404(char_id)

    # Only allow copying public characters or own characters
    if not original.is_public and original.owner_id != current_user.id:
        flash("You cannot copy this character.", "danger")
        return redirect(url_for('main.public_characters'))

    new_character = Character(
        name=f"{original.name} (Copy)",
        race=original.race,
        character_class=original.character_class,
        background=original.background,
        backstory=original.backstory,
        strength=original.strength,
        dexterity=original.dexterity,
        constitution=original.constitution,
        intelligence=original.intelligence,
        wisdom=original.wisdom,
        charisma=original.charisma,
        owner=current_user,
        is_public=False
    )

    db.session.add(new_character)
    db.session.commit()

    flash(f"Copied '{original.name}' to your characters!", "success")
    return redirect(url_for('main.edit_character', character_id=new_character.id))

# ------------------ Character Lists ------------------

@main.route('/my_characters')
@login_required
def my_characters():
    characters = Character.query.filter_by(user_id=current_user.id).all()
    return render_template('character_list.html', characters=characters, personal=True)


@main.route('/public_characters')
@login_required
def public_characters():
    characters = Character.query.filter_by(is_public=True).filter(Character.user_id != current_user.id).all()
    return render_template('character_list.html', characters=characters, personal=False)

# ------------------ Character Detail ------------------

@main.route('/character/<int:char_id>')
@login_required
def character_detail(char_id):
    character = Character.query.get_or_404(char_id)
    if not character.is_public and character.user_id != current_user.id:
        flash("You cannot view this character")
        return redirect(url_for('main.dashboard'))
    return render_template('character_detail.html', character=character)
