# fingertraining
# Stefan Hochuli, 31.08.2021,
# Folder:  File: add_data.py
#

from speck_weg.models import (TrainingThemeModel, TrainingProgramModel, TrainingExerciseModel,
                              TrainingProgramExerciseModel, UserModel)

from speck_weg.db import CRUD

if __name__ == '__main__':
    db = CRUD(drop_all=True)

    usr1 = UserModel(name='Stefan', weight=72)
    tth1 = TrainingThemeModel(name='Beastmaker 1000', sequence=1)
    tpr1 = TrainingProgramModel(name='5a', sequence=2, training_theme=tth1)
    tpr2 = TrainingProgramModel(name='5b', sequence=3, training_theme=tth1)
    tpr3 = TrainingProgramModel(name='5c', sequence=4, training_theme=tth1)
    tex1 = TrainingExerciseModel(name='Jugs', baseline_sets=1, baseline_repetitions=7, baseline_duration=7, user=usr1)
    tex2 = TrainingExerciseModel(name='Open 3 tief', baseline_sets=1, baseline_repetitions=7, baseline_duration=7, user=usr1)
    tex3 = TrainingExerciseModel(name='Open 4 tief', baseline_sets=1, baseline_repetitions=7, baseline_duration=7, user=usr1)
    tex4 = TrainingExerciseModel(name='Half Crimp tief', description='Vorderstes Glied', baseline_sets=1, baseline_repetitions=7,
                                 baseline_duration=7, user=usr1)
    tex5 = TrainingExerciseModel(name='Sloper 20°', baseline_sets=1, baseline_repetitions=7, baseline_duration=7, user=usr1)
    tex6 = TrainingExerciseModel(name='Open 3 mittel', baseline_sets=1, baseline_repetitions=7, baseline_duration=7, user=usr1)
    tex7 = TrainingExerciseModel(name='Open 2 tief (Zeig-/Mittelfinger)',
                                 description='Zeige- / Mittelfinger oder Mittel- / Ringfinger',
                                 baseline_sets=1, baseline_repetitions=7, baseline_duration=7, user=usr1)
    tex8 = TrainingExerciseModel(name='Open 4 halb-tief ', description='Vorderstes Glied',
                                 baseline_sets=1, baseline_repetitions=7, baseline_duration=7, user=usr1)
    tex9 = TrainingExerciseModel(name='Open 4 mittel', baseline_sets=1, baseline_repetitions=7, baseline_duration=7, user=usr1)

    # 5a
    tpe1 = TrainingProgramExerciseModel(training_program=tpr1, training_exercise=tex1, sequence=1)
    tpe2 = TrainingProgramExerciseModel(training_program=tpr1, training_exercise=tex1, sequence=2)
    tpe3 = TrainingProgramExerciseModel(training_program=tpr1, training_exercise=tex2, sequence=3)
    tpe4 = TrainingProgramExerciseModel(training_program=tpr1, training_exercise=tex2, sequence=4)
    tpe5 = TrainingProgramExerciseModel(training_program=tpr1, training_exercise=tex3, sequence=5)
    tpe6 = TrainingProgramExerciseModel(training_program=tpr1, training_exercise=tex3, sequence=6)
    # 5b
    tpe7 = TrainingProgramExerciseModel(training_program=tpr2, training_exercise=tex4, sequence=1)
    tpe8 = TrainingProgramExerciseModel(training_program=tpr2, training_exercise=tex5, sequence=2)
    tpe9 = TrainingProgramExerciseModel(training_program=tpr2, training_exercise=tex4, sequence=3)
    tpe10 = TrainingProgramExerciseModel(training_program=tpr2, training_exercise=tex6, sequence=4)
    tpe11 = TrainingProgramExerciseModel(training_program=tpr2, training_exercise=tex7, sequence=5)
    tpe12 = TrainingProgramExerciseModel(training_program=tpr2, training_exercise=tex8, sequence=6)
    # 5c
    tpe13 = TrainingProgramExerciseModel(training_program=tpr3, training_exercise=tex4, sequence=1)
    tpe14 = TrainingProgramExerciseModel(training_program=tpr3, training_exercise=tex6, sequence=2)
    tpe15 = TrainingProgramExerciseModel(training_program=tpr3, training_exercise=tex9, sequence=3)
    tpe16 = TrainingProgramExerciseModel(training_program=tpr3, training_exercise=tex7, sequence=4)
    tpe17 = TrainingProgramExerciseModel(training_program=tpr3, training_exercise=tex5, sequence=5)
    tpe18 = TrainingProgramExerciseModel(training_program=tpr3, training_exercise=tex9, sequence=6)

    # Warmup
    tpr4 = TrainingProgramModel(name='Warmup Schultern / Arme', training_theme=tth1, sequence=1)
    tex10 = TrainingExerciseModel(name='Terraband diagonal', baseline_sets=3, baseline_repetitions=10)
    tex11 = TrainingExerciseModel(name='Terraband Schulter 1/4 Drehung', baseline_sets=3, baseline_repetitions=10)
    tex12 = TrainingExerciseModel(name='Terraband Ellbogen 1/4 Drehung', baseline_sets=3, baseline_repetitions=10)
    tex13 = TrainingExerciseModel(name='Liegestützen', baseline_sets=3, baseline_repetitions=10)
    tex14 = TrainingExerciseModel(name='Schulter anspannen 2 Arme', description='3s halten', baseline_sets=3, baseline_repetitions=10, user=usr1)
    tex15 = TrainingExerciseModel(name='Schulter anspannen 1 Arm', description='3s halten', baseline_sets=3, baseline_repetitions=5, user=usr1)
    tex16 = TrainingExerciseModel(name='Klimmzug', baseline_sets=3, baseline_repetitions=5, user=usr1)
    tpe19 = TrainingProgramExerciseModel(training_program=tpr4, training_exercise=tex10, sequence=1)
    tpe20 = TrainingProgramExerciseModel(training_program=tpr4, training_exercise=tex11, sequence=2)
    tpe21 = TrainingProgramExerciseModel(training_program=tpr4, training_exercise=tex12, sequence=3)
    tpe22 = TrainingProgramExerciseModel(training_program=tpr4, training_exercise=tex13, sequence=4)
    tpe23 = TrainingProgramExerciseModel(training_program=tpr4, training_exercise=tex14, sequence=5)
    tpe24 = TrainingProgramExerciseModel(training_program=tpr4, training_exercise=tex15, sequence=6)
    tpe25 = TrainingProgramExerciseModel(training_program=tpr4, training_exercise=tex16, sequence=7)

    objects = [
        usr1,
        tth1,
        tpr1,
        tpr2,
        tpr3,
        tex1,
        tex2,
        tex3,
        tex4,
        tex5,
        tex6,
        tex7,
        tex8,
        tex9,
        tpe1,
        tpe2,
        tpe3,
        tpe4,
        tpe5,
        tpe6,
        tpe7,
        tpe8,
        tpe9,
        tpe10,
        tpe11,
        tpe12,
        tpe13,
        tpe14,
        tpe15,
        tpe16,
        tpe17,
        tpe18,
        tpr4,
        tex10,
        tex11,
        tex12,
        tex13,
        tex14,
        tex15,
        tpe19,
        tpe20,
        tpe21,
        tpe22,
        tpe23,
        tpe24,
    ]
    db.create(objects)
