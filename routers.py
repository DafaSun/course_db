import gloval_var
from models import *
from gloval_var import *
from datetime import datetime


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/registration_', methods=['POST'])
def registration_():
    login = request.form['login_field']
    password = request.form['password_field']

    added_successfully = True
    # Проверка уникальности перед добавлением в базу данных
    if User.select().where(User.login == login).exists():
        added_successfully = False

    if added_successfully:
        User.create(login=login, password=password)
        user = User.get((User.login == login) & (User.password == password))
        gloval_var.user_id = user.get_id()

    return render_template('registration.html', added_successfully=added_successfully)


@app.route('/entrance')
def entrance():
    return render_template("entrance.html")


@app.route('/entrance_', methods=['POST'])
def entrance_():
    login = request.form['login_field']
    password = request.form['password_field']

    password_true = False
    if User.select().where(User.login == login and User.password == password).exists():
        password_true = True
        user = User.get((User.login == login) & (User.password == password))
        gloval_var.user_id = user.get_id()

    return render_template('entrance.html', password_true=password_true)


@app.route('/main')
def main():
    return render_template("main.html")


@app.route('/useful_inform')
def useful_inform():
    return render_template("useful_inform.html")


@app.route('/add_inform')
def add_inform():
    return render_template("add_inform.html")


@app.route('/add_person_page')
def add_person_page():
    return render_template('add_about_person.html', good=None)


@app.route('/add_person', methods=['POST'])
def add_person():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    middle_name = request.form['middle_name']
    if (middle_name == ''):
        middle_name = None

    maiden_name = request.form['maiden_name']
    if (maiden_name == ''):
        maiden_name = None

    selected_gender = request.form.get('gender')
    if selected_gender == 'male':
        gender = Gender.get(Gender.gender_name == 'Мужской')
    else:
        gender = Gender.get(Gender.gender_name == 'Женский')

    birthday_str = request.form.get('birthday')
    if birthday_str != '':
        birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
    else:
        birthday = None

    die_day_str = request.form.get('die_day')
    if die_day_str != '':
        die_day = datetime.strptime(die_day_str, '%Y-%m-%d').date()
    else:
        die_day = None

    try:
        fcs = FCS.create(name=first_name, surname=last_name, patronymic=middle_name, maiden_name=maiden_name)
        person = Person.create(fcs=fcs, gender=gender, birthday=birthday, day_of_die=die_day)
        u = gloval_var.user_id
        p = person.id
        print(u)
        print(p)
        belonging = Belonging_to_user.create(user_id=u, person_id=p)
    except DataError:
        print('0')
        return render_template('add_about_person.html', good=0)

    contactData = request.form.get('contactData')
    if contactData == 'true':
        phone_number = request.form['phone_number']
        if (phone_number == ''):
            phone_number = None
        email = request.form['email']
        if (email == ''):
            email = None
        try:
            contact = ContactData.create(person=person, phone_number=phone_number, email=email)
        except DataError:
            print('1')
            return render_template('add_about_person.html', good=0)

    education = request.form.get('education')
    if education == 'true':
        e_selected_level = request.form['e_level']
        if e_selected_level == 'u1':
            e_level = EducationLevel.get(EducationLevel.level_name == 'Начальное')
        elif e_selected_level == 'u2':
            e_level = EducationLevel.get(EducationLevel.level_name == 'Основное общее')
        elif e_selected_level == 'u3':
            e_level = EducationLevel.get(EducationLevel.level_name == 'Среднее общее')
        elif e_selected_level == 'u4':
            e_level = EducationLevel.get(EducationLevel.level_name == 'Среднее профессиональное')
        else:
            e_level = EducationLevel.get(EducationLevel.level_name == 'Высшее')

        e_profession = request.form['e_profession']
        e_time_begin_str = request.form['e_time_begin']
        if e_time_begin_str != '':
            e_time_begin = datetime.strptime(e_time_begin_str, '%Y-%m-%d').date()
        else:
            e_time_begin = None
        e_time_end_str = request.form['e_time_end']
        if e_time_end_str != '':
            e_time_end = datetime.strptime(e_time_end_str, '%Y-%m-%d').date()
        else:
            e_time_end = None
        e_organisation = request.form['e_organisation']
        if (e_organisation == ''):
            e_organisation = None
        e_country = request.form['e_country']
        if (e_country == ''):
            e_country = None
        e_region = request.form['e_region']
        if (e_region == ''):
            e_region = None
        e_city = request.form['e_city']
        if (e_city == ''):
            e_city = None
        e_street = request.form['e_street']
        if (e_street == ''):
            e_street = None
        e_house_str = request.form['e_house']
        if (e_house_str == ''):
            e_house = None
        else:
            e_house = int(e_house_str)
        try:
            e_time = TimeInterval.create(begin_time=e_time_begin, end_time=e_time_end)
            e_address = Address.create(country=e_country, region=e_region, city=e_city, street=e_street,
                                       house=e_house)
            e_organisation = Organisation.create(organisation_name=e_organisation, address=e_address)
            e_education = Education.create(education_organisation=e_organisation, profession=e_profession,
                                           level=e_level,
                                           time=e_time,
                                           person=person)
        except DataError as e:
            print(f"Произошла ошибка данных: {e}")
            print('2')
            return render_template('add_about_person.html', good=0)

    work = request.form.get('work')
    if work == 'true':
        w_post = request.form['w_post']
        if (w_post == ''):
            w_post = None
        w_time_begin_str = request.form['w_time_begin']
        if w_time_begin_str != '':
            w_time_begin = datetime.strptime(w_time_begin_str, '%Y-%m-%d').date()
        else:
            w_time_begin = None
        w_time_end_str = request.form['w_time_end']
        if w_time_end_str != '':
            w_time_end = datetime.strptime(w_time_end_str, '%Y-%m-%d').date()
        else:
            w_time_end = None
        w_organisation = request.form['w_organisation']
        if (w_organisation == ''):
            w_organisation = None
        w_country = request.form['w_country']
        if (w_country == ''):
            w_country = None
        w_region = request.form['w_region']
        if (w_region == ''):
            w_region = None
        w_city = request.form['w_city']
        if (w_city == ''):
            w_city = None
        w_street = request.form['w_street']
        if (w_street == ''):
            w_street = None
        w_house_str = request.form['w_house']
        if (w_house_str == ''):
            w_house = None
        else:
            w_house = int(w_house_str)
        try:
            w_time = TimeInterval.create(begin_time=w_time_begin, end_time=w_time_end)
            w_address = Address.create(country=w_country, region=w_region, city=w_city, street=w_street,
                                       house=w_house)
            w_organisation = Organisation.create(organisation_name=w_organisation, address=w_address)
            w_work = Work.create(organisation=w_organisation, post=w_post, time=w_time, person=person)
        except DataError:
            print('3')
            return render_template('add_about_person.html', good=0)

    residence = request.form.get('residence')
    if residence == 'true':
        r_country = request.form['r_country']
        if (r_country == ''):
            r_country = None
        r_region = request.form['r_region']
        if (r_region == ''):
            r_region = None
        r_city = request.form['r_city']
        if (r_city == ''):
            r_city = None
        r_street = request.form['r_street']
        if (r_street == ''):
            r_street = None
        r_house_str = request.form['r_house']
        if (r_house_str == ''):
            r_house = None
        else:
            r_house = int(r_house_str)
        r_flat_str = request.form['r_flat']
        if (r_flat_str == ''):
            r_flat = None
        else:
            r_flat = int(r_flat_str)
        r_time_begin_str = request.form['r_time_begin']
        if r_time_begin_str != '':
            r_time_begin = datetime.strptime(r_time_begin_str, '%Y-%m-%d').date()
        else:
            r_time_begin = None
        r_time_end_str = request.form['r_time_end']
        if r_time_end_str != '':
            r_time_end = datetime.strptime(r_time_end_str, '%Y-%m-%d').date()
        else:
            r_time_end = None
        try:
            r_time = TimeInterval.create(begin_time=r_time_begin, end_time=r_time_end)
            r_address = Address.create(country=r_country, region=r_region, city=r_city, street=r_street,
                                       house=r_house,
                                       flat=r_flat)
            r_residence = Residence.create(address=r_address, time=r_time, person_id=person)
        except DataError:
            print('4')
            return render_template('add_about_person.html', good=0)

    marriage = request.form.get('marriage')
    if marriage == 'true':
        m_person = request.form['m_person']
        m_time_begin_str = request.form['m_time_begin']
        if m_time_begin_str != '':
            m_time_begin = datetime.strptime(m_time_begin_str, '%Y-%m-%d').date()
        else:
            m_time_begin = None
        m_time_end_str = request.form['m_time_end']
        if m_time_end_str != '':
            m_time_end = datetime.strptime(m_time_end_str, '%Y-%m-%d').date()
        else:
            m_time_end = None
        try:
            m_time = TimeInterval.create(begin_time=m_time_begin, end_time=m_time_end)
            if selected_gender == 'male':
                m_marriage = Marriage.create(husband=person, time=m_time, wife=m_person)
            else:
                m_marriage = Marriage.create(husband=m_person, time=m_time, wife=person)
        except DataError:
            print('5')
            return render_template('add_about_person.html', good=0)

    children = request.form.get('children')
    if children == 'true':
        p_mom = request.form['p_mom']
        if (p_mom != ''):
            try:
                p1 = TimeInterval.create(parent=p_mom, children=person)
            except DataError:
                print('6')
                return render_template('add_about_person.html', good=0)
        p_dad = request.form['p_dad']
        if (p_dad != ''):
            try:
                p2 = TimeInterval.create(parent=p_dad, children=person)
            except DataError:
                print('6')
                return render_template('add_about_person.html', good=0)

    return render_template('add_about_person.html', good=1)


@app.route('/update_about_person')
def update_about_person():
    return render_template("update_about_person.html", good=None)


@app.route('/add_education_page')
def add_education_page():
    return render_template("add_education.html", good=None)


@app.route('/add_education', methods=['POST'])
def add_education():
    person_str = request.form.get('person')
    person = Person.get_by_id(int(person_str))
    e_selected_level = request.form['e_level']
    if e_selected_level == 'u1':
        e_level = EducationLevel.get(EducationLevel.level_name == 'Начальное')
    elif e_selected_level == 'u2':
        e_level = EducationLevel.get(EducationLevel.level_name == 'Основное общее')
    elif e_selected_level == 'u3':
        e_level = EducationLevel.get(EducationLevel.level_name == 'Среднее общее')
    elif e_selected_level == 'u4':
        e_level = EducationLevel.get(EducationLevel.level_name == 'Среднее профессиональное')
    else:
        e_level = EducationLevel.get(EducationLevel.level_name == 'Высшее')

    e_profession = request.form['e_profession']
    e_time_begin_str = request.form['e_time_begin']
    if e_time_begin_str != '':
        e_time_begin = datetime.strptime(e_time_begin_str, '%Y-%m-%d').date()
    else:
        e_time_begin = None
    e_time_end_str = request.form['e_time_end']
    if e_time_end_str != '':
        e_time_end = datetime.strptime(e_time_end_str, '%Y-%m-%d').date()
    else:
        e_time_end = None
    e_organisation = request.form['e_organisation']
    if (e_organisation == ''):
        e_organisation = None
    e_country = request.form['e_country']
    if (e_country == ''):
        e_country = None
    e_region = request.form['e_region']
    if (e_region == ''):
        e_region = None
    e_city = request.form['e_city']
    if (e_city == ''):
        e_city = None
    e_street = request.form['e_street']
    if (e_street == ''):
        e_street = None
    e_house_str = request.form['e_house']
    if (e_house_str == ''):
        e_house = None
    else:
        e_house = int(e_house_str)
    try:
        e_time = TimeInterval.create(begin_time=e_time_begin, end_time=e_time_end)
        e_address = Address.create(country=e_country, region=e_region, city=e_city, street=e_street,
                                   house=e_house)
        e_organisation = Organisation.create(organisation_name=e_organisation, address=e_address)
        e_education = Education.create(education_organisation=e_organisation, profession=e_profession,
                                       level=e_level,
                                       time=e_time,
                                       person=person)
        return render_template('add_education.html', good=1)
    except DataError as e:
        print(f"Произошла ошибка: {e}")
        return render_template('add_education.html', good=0)



@app.route('/add_work_page')
def add_work_page():
    return render_template("add_work.html", good=None)


@app.route('/add_work', methods=['POST'])
def add_work():
    person_str = request.form.get('person')
    person = Person.get_by_id(int(person_str))
    w_post = request.form['w_post']
    if (w_post == ''):
        w_post = None
    w_time_begin_str = request.form['w_time_begin']
    if w_time_begin_str != '':
        w_time_begin = datetime.strptime(w_time_begin_str, '%Y-%m-%d').date()
    else:
        w_time_begin = None
    w_time_end_str = request.form['w_time_end']
    if w_time_end_str != '':
        w_time_end = datetime.strptime(w_time_end_str, '%Y-%m-%d').date()
    else:
        w_time_end = None
    w_organisation = request.form['w_organisation']
    if (w_organisation == ''):
        w_organisation = None
    w_country = request.form['w_country']
    if (w_country == ''):
        w_country = None
    w_region = request.form['w_region']
    if (w_region == ''):
        w_region = None
    w_city = request.form['w_city']
    if (w_city == ''):
        w_city = None
    w_street = request.form['w_street']
    if (w_street == ''):
        w_street = None
    w_house_str = request.form['w_house']
    if (w_house_str == ''):
        w_house = None
    else:
        w_house = int(w_house_str)
    try:
        w_time = TimeInterval.create(begin_time=w_time_begin, end_time=w_time_end)
        w_address = Address.create(country=w_country, region=w_region, city=w_city, street=w_street,
                                   house=w_house)
        w_organisation = Organisation.create(organisation_name=w_organisation, address=w_address)
        w_work = Work.create(organisation=w_organisation, post=w_post, time=w_time, person=person)
        return render_template('add_work.html', good=1)
    except DataError as e:
        print(f"Произошла ошибка: {e}")
        return render_template('add_work.html', good=0)



@app.route('/add_residence_page')
def add_residence_page():
    return render_template("add_residence.html", good=None)


@app.route('/add_residence', methods=['POST'])
def add_residence():
    person_str = request.form.get('person')
    person = Person.get_by_id(int(person_str))
    r_country = request.form['r_country']
    if (r_country == ''):
        r_country = None
    r_region = request.form['r_region']
    if (r_region == ''):
        r_region = None
    r_city = request.form['r_city']
    if (r_city == ''):
        r_city = None
    r_street = request.form['r_street']
    if (r_street == ''):
        r_street = None
    r_house_str = request.form['r_house']
    if (r_house_str == ''):
        r_house = None
    else:
        r_house = int(r_house_str)
    r_flat_str = request.form['r_flat']
    if (r_flat_str == ''):
        r_flat = None
    else:
        r_flat = int(r_flat_str)
    r_time_begin_str = request.form['r_time_begin']
    if r_time_begin_str != '':
        r_time_begin = datetime.strptime(r_time_begin_str, '%Y-%m-%d').date()
    else:
        r_time_begin = None
    r_time_end_str = request.form['r_time_end']
    if r_time_end_str != '':
        r_time_end = datetime.strptime(r_time_end_str, '%Y-%m-%d').date()
    else:
        r_time_end = None
    try:
        r_time = TimeInterval.create(begin_time=r_time_begin, end_time=r_time_end)
        r_address = Address.create(country=r_country, region=r_region, city=r_city, street=r_street,
                                   house=r_house,
                                   flat=r_flat)
        r_residence = Residence.create(address=r_address, time=r_time, person_id=person)
        return render_template('add_residence.html', good=1)
    except DataError:
        print('4')
        return render_template('add_residence.html', good=0)


@app.route('/add_marriade_page')
def add_marriage_page():
    return render_template("add_marriage.html", good=None)


@app.route('/add_marriade', methods=['POST'])
def add_marriage():
    person_str = request.form.get('person')
    try:
        person = Person.get_by_id(int(person_str))
        if (Belonging_to_user.get(Belonging_to_user.person_id == int(person_str))):
            m_person = request.form['m_person']
            m_time_begin_str = request.form['m_time_begin']
            if m_time_begin_str != '':
                m_time_begin = datetime.strptime(m_time_begin_str, '%Y-%m-%d').date()
            else:
                m_time_begin = None
            m_time_end_str = request.form['m_time_end']
            if m_time_end_str != '':
                m_time_end = datetime.strptime(m_time_end_str, '%Y-%m-%d').date()
            else:
                m_time_end = None
            try:
                m_time = TimeInterval.create(begin_time=m_time_begin, end_time=m_time_end)
                if person.gender == 'Мужской':
                    m_marriage = Marriage.create(husband=person, time=m_time, wife=m_person)
                else:
                    m_marriage = Marriage.create(husband=m_person, time=m_time, wife=person)
                return render_template('add_marriage.html', good=1)
            except DataError:
                print('5')
                return render_template('add_marriage.html', good=0)
    except DoesNotExist:
        print('5')
        return render_template('add_marriage.html', good=0)


@app.route('/add_contact_page')
def add_contact_page():
    return render_template("add_contact.html", good=None)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    person_str = request.form.get('person')
    try:
        person = Person.get_by_id(int(person_str))
        if (Belonging_to_user.get(Belonging_to_user.person_id == int(person_str))):
            phone_number = request.form['phone_number']
            if (phone_number == ''):
                phone_number = None
            email = request.form['email']
            if (email == ''):
                email = None
            try:
                contact = ContactData.create(person=person, phone_number=phone_number, email=email)
                return render_template('add_contact.html', good=1)
            except DataError:
                print('1')
                return render_template('add_contact.html', good=0)
    except DoesNotExist:
        print('1')
        return render_template('add_contact.html', good=0)


@app.route('/delete_about_person')
def delete_about_person():
    person_id = request.form.get('person')
    try:
        person = Person.get_by_id(int(person_id))
        if (Belonging_to_user.get(Belonging_to_user.person_id == int(person_id))):
            try:
                c = ContactData.select().where(ContactData.person == int(person_id))
                for element in c:
                    element.delete_instance()
            except DoesNotExist:
                return render_template('delete_about_person.html', delete=0)

            try:
                e = Education.select().where(Education.person_id == int(person_id))
                for element in e:
                    element.delete_instance()
            except DoesNotExist:
                return render_template('delete_about_person.html', delete=0)

            try:
                w = Work.filter(Work.person_id == int(person_id))
                for element in w:
                    element.delete_instance()
            except DoesNotExist:
                return render_template('delete_about_person.html', delete=0)

            try:
                r = Residence.select().where(Residence.person_id == int(person_id))
                for element in r:
                    element.delete_instance()
            except DoesNotExist:
                return render_template('delete_about_person.html', delete=0)

            try:
                m = Marriage.select().where((Marriage.husband == int(person_id)) or (Marriage.wife == int(person_id)))
                for element in m:
                    element.delete_instance()
            except DoesNotExist:
                return render_template('delete_about_person.html', delete=0)

            try:
                ch = Children.select().where(
                    (Children.parent_id == int(person_id)) or (Children.child_id == int(person_id)))
                for element in ch:
                    element.delete_instance()
            except DoesNotExist:
                return render_template('delete_about_person.html', delete=0)

            try:
                person = Person.delete_by_id(int(person_id))
                return render_template('delete_about_person.html', delete=1)
            except DoesNotExist:
                return render_template('delete_about_person.html', delete=0)
        else:
            return render_template('delete_about_person.html', delete=-1)
    except DoesNotExist:
        return render_template('delete_about_person.html', delete=0)


@app.route('/add_story_page')
def add_story_page():
    return render_template('add_story.html', good=None)


@app.route('/add_story', methods=['POST'])
def add_story():
    try:
        person = request.form['person']
        if person == '':
            p = None
        else:
            p = Person.get_by_id(int(person))

        date_str = request.form['date']
        if date_str != '':
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = None

        text = request.form['textInput']

        name = request.form['name']
        if (name == ''):
            name = None

        story = Story.create(date=date, person=p, story=text, user=gloval_var.user_id)
    except DataError:
        print('5')
        return render_template('add_story.html', good=0)
    except DoesNotExist:
        print('5')
        return render_template('add_story.html', good=-1)

    return render_template('add_story.html', good=1)


@app.route('/delete_story')
def delete_story():
    story_id = request.args.get('person_id')
    story = Story.get_by_id(story_id)
    try:
        if (story.user == gloval_var.user_id):
            if story_id:
                try:
                    p = Story.get_by_id(int(story_id))
                    story = p.delete_instance()
                    return render_template('delete_story.html', delete=1)
                except DoesNotExist:
                    return render_template('delete_story.html', delete=0)
            else:
                return render_template('delete_story.html', delete=-1)
    except DoesNotExist:
        return render_template('delete_story.html', delete=-1)


@app.route('/get_inform')
def get_inform():
    return render_template("get_inform.html")


@app.route('/get_person', methods=['GET'])
def get_person():
    person_id = request.args.get('person_id')
    if person_id:
        try:
            person = Person.get_by_id(int(person_id))
            contact = ContactData.select().where(ContactData.person == int(person_id))
            education = Education.select().where(Education.person_id == int(person_id))
            work = Work.select().where(Work.person_id == int(person_id))
            residence = Residence.select().where(Residence.person_id == int(person_id))
            marriage = Marriage.select().where(
                (Marriage.husband == int(person_id)) or (Marriage.wife == int(person_id)))
            parent = Children.select().where(Children.child_id == int(person_id))
            return render_template('get_about_person.html', person=person, contact=contact, education=education,
                                   work=work, residence=residence, marriage=marriage, person_id=person,
                                   parent=parent)
        except Person.DoesNotExist:
            return render_template('get_about_person.html', person=None, contact=None, education=None,
                                   work=None,
                                   residence=None, marriage=None, person_id=None, parent=None)
    else:
        return render_template('get_about_person.html', person=None, contact=None, education=None, work=None,
                               residence=None, marriage=None, person_id=None, parent=None)


@app.route('/get_all_people')
def get_all_people():
    people = Person.select()
    return render_template('all_inform.html', people=people)


@app.route('/cities')
def cities():
    table = (Residence.select()
             .join(Address, on=(Residence.address == Address.id))
             .distinct())
    return render_template("cities.html", table=table)


@app.route('/birthday')
def birthday():
    date1 = Person.select()
    return render_template("birthday.html", date1=date1)


@app.route('/children')
def children():
    person_id = request.args.get('person_id')
    if person_id:
        try:
            children = Children.select()\
                .where(Children.parent_id == int(person_id))
            return render_template('children.html', children=children)
        except Person.DoesNotExist:
            return render_template('children.html', children=None)
    else:
        return render_template('children.html', children=None)


@app.route('/dates')
def dates():
    date1 = Person.select()
    date_marriage = Marriage.select()
    return render_template("dates.html", date1=date1, date_marriage=date_marriage)


@app.route('/story')
def story():
    story = Story.select()
    return render_template("story.html", story=story)


@app.route('/story_by_id')
def story_by_id():
    person_id = request.form.get('person')
    person = Person.get_by_id(int(person_id))
    if person_id:
        try:
            return render_template('story_by_id.html', story=story)
        except DoesNotExist:
            return render_template('story_by_id.html', story=None)
    else:
        return render_template('story_by_id.html', story=None)

# @app.route('/main')
# def main():
#     return render_template("main.html")
#
#
# @app.route('/add_inform')
# def add_inform():
#     return render_template("add_inform.html")
#
#
# @app.route('/add_about_person')
# def add_about_person():
#     return render_template("add_about_person.html")
#
#
# @app.route('/add_about_person_', methods=['POST'])
# def add_about_person_():
#     name = request.form['name']
#     surname = request.form['surname']
#     maiden_name = request.form['maiden_name']
#     patronymic = request.form['patronymic']
#     gender_ = request.form['gender']
#     birthday_str = request.form['birthday']
#     birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date() if birthday_str else None
#     date_of_die_str = request.form['date_of_die']
#     date_of_die = datetime.strptime(birthday_str, '%Y-%m-%d').date() if birthday_str else None
#     phone_number = request.form['phone_number']
#     email = request.form['email']
#
#     if gender_ == 'male':
#         gender = gender = Gender.get(Gender.gender_name == 'Мужской')
#     else:
#         gender = Gender.get(Gender.gender_name == 'Женский')
#     fcs = FCS.create()
#     person = Person.create(fcs=fcs, gender=gender, birthday=birthday, date_of_die=date_of_die)
#     contact = ContactData.create(phone_number=phone_number, email=email, person=person)
#
#     return redirect(url_for('add_about_person'))
#
#
# @app.route('/update_about_person')
# def update_about_person():
#     return render_template("update_about_person.html")
#
#
# @app.route('/delete_about_person')
# def delete_about_person():
#     return render_template("delete_about_person.html")
#
#
# @app.route('/add_story')
# def add_story():
#     return render_template("add_story.html")
#
#
# @app.route('/update_story')
# def update_story():
#     return render_template("update_story.html")
#
#
# @app.route('/delete_story')
# def delete_story():
#     return render_template("delete_story.html")
#
#
# @app.route('/get_inform')
# def get_inform():
#     return render_template("get_inform.html")
#
#
#
# @app.route('/get_about_person', methods=['GET'])
# def get_about_person():
#     person_id = request.args.get('person_id')
#     if person_id:
#         try:
#             person = Person.get_by_id(int(person_id))
#             return render_template('get_about_person.html', person=person)
#         except Person.DoesNotExist:
#             return render_template('get_about_person.html', person=None)
#     else:
#         return render_template('get_about_person.html', person=None)
#
#
#
#
# @app.route('/all_inform')
# def all_inform():
#     return render_template("all_inform.html")
#
#
# @app.route('/birthday')
# def birthday():
#     return render_template("birthday.html")
#
#
# @app.route('/children')
# def children():
#     return render_template("children.html")
#
#
# @app.route('/cities')
# def cities():
#     table = Address \
#         .select(Address.city) \
#         .join(Residence, on=(Address.id == Residence.address)) \
#         .group_by(Address.city)
#     return render_template("cities.html", table=table)
#
#
# @app.route('/dates')
# def dates():
#     return render_template("dates.html")
#
#
# @app.route('/story')
# def story():
#     return render_template("story.html")
#
#
# @app.route('/story_by_id')
# def story_by_id():
#     return render_template("story_by_id.html")
