# вставка начальных данных
from sqlalchemy.orm import Session
from database import engine
import models
from datetime import date

with Session(bind=engine) as session:
    climber1 = models.Climber(surname='Иванов', name='Степан',  patronymic='Олегович', address='г. Нижний Тагил, ул. Ленина, 19')
    climber2 = models.Climber(surname='Суворов', name='Егор',  patronymic='Денисович', address='г. Балашиха, наб. Будапештская, 61')
    climber3 = models.Climber(surname='Сидоров', name='Артем',  patronymic='Юрьевич', address='г. Шаховская, пр. 1905 года, 92')
    climber4 = models.Climber(surname='Макарова', name='Анна',  patronymic='Юрьевна', address='г. Солнечногорск, пр. Космонавтов, 47')
    climber5 = models.Climber(surname='Фадеев', name='Кирилл',  patronymic='Владимрович', address='г. Воскресенск, ул. Гагарина, 96')
    climber6 = models.Climber(surname='Князева', name='Светлана',  patronymic='Андреевна', address='г. Чехов, пр. Строителей, 25')

    climbing1 = models.Climbing(date_start=date(2017,8,10), date_end=date(2017,8,20), name_group ="Группа1", mountain_id=1,climbers=[climber1, climber2, climber3])
    climbing2 = models.Climbing(date_start=date(2017,9,23), date_end=date(2017,10,5),  name_group ="Группа2", mountain_id=2,climbers=[climber2, climber3, climber4, climber5])
    climbing3 = models.Climbing(date_start=date(2018,3,1), date_end=date(2018,3,19), name_group ="Группа3", mountain_id=1,climbers=[climber1, climber2, climber3, climber6])
    
    mountain1 = models.Mountain(name='Белая', height=715, country_district='Россия, Свердловкая обл.')
    mountain2 = models.Mountain(name='Белуха', height=4506, country_district='Россия, Усть-Коксинский район')
    mountain3 = models.Mountain(name='Шхара', height=5193.2, country_district='Россия, Свердловкая обл.')
    mountain4 = models.Mountain(name='Джимара', height=4780, country_district='Россия, Большой Кавказ')
    mountain5 = models.Mountain(name='Саухох', height=4636, country_district='Россия, Северная Осетия')
    
    session.add_all([climber1, climber2, climber3, climber4, climber5, climber6, climbing1, climbing2, climbing3, mountain1, mountain2, mountain3, mountain4, mountain5])
    session.commit()