from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.postgres_db.postgres_database import get_db
from app.domain.models.fitplan_model import (Coach,
                                             CoachMetrics,
                                             Present,
                                             WorkoutPlan,
                                             Take,
                                             User, UserRequestMeal, UserMeal,
                                             UserMealMealSupplement, MealSupplement, WorkoutPlanMealSupplement,
                                             UserRequestExercise, UserExercise, UserExerciseExercise, Exercise,
                                             WorkoutPlanExercise)

from app.domain.models.fitplan_model import (CoachPlanPrice, GymPlanPrice,
                                             Gym)


class CoachRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def create_coach(self, coach: Coach) -> Coach:
        self.db.add(coach)
        self.db.commit()
        self.db.refresh(coach)
        logger.info(f"[+] Coach Created With Id ---> {coach.id} And Email ---> {coach.email}")
        return coach

    def create_coach_metrics(self, metrics: CoachMetrics) -> CoachMetrics:
        self.db.add(metrics)
        self.db.commit()
        self.db.refresh(metrics)
        logger.info(f"[+] Metrics Created For Coach Id ---> {metrics.coach_id}")
        return metrics

    def update_coach(self, coach_id: int, updated_coach: Dict):
        coach_query = self.db.query(Coach).filter(Coach.id == coach_id)
        db_coach = coach_query.first()
        coach_query.filter(Coach.id == coach_id).update(
            updated_coach, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_coach)
        logger.info(f"[+] Coach With Id ---> {coach_id} Updated")
        return db_coach

    def update_coach_metrics(self, coach_id: int, updated_metrics: Dict):
        metrics_query = self.db.query(CoachMetrics).filter(CoachMetrics.coach_id == coach_id)
        db_metrics = metrics_query.first()
        if not db_metrics:
            logger.warning(f"[-] Metrics For Coach Id ---> {coach_id} Not Found")
            return None
        metrics_query.update(updated_metrics, synchronize_session=False)
        self.db.commit()
        self.db.refresh(db_metrics)
        logger.info(f"[+] Metrics For Coach Id ---> {coach_id} Updated")
        return db_metrics

    def update_coach_by_email(self, coach_email: str, updated_coach: Dict):
        coach_query = self.db.query(Coach).filter(Coach.email == coach_email)
        db_coach = coach_query.first()
        coach_query.filter(Coach.email == coach_email).update(
            updated_coach, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_coach)
        logger.info(f"[+] Coach With Email ---> {coach_email} Updated")
        return db_coach

    def delete_coach(self, coach: Coach) -> None:
        self.db.delete(coach)
        self.db.commit()
        self.db.flush()
        logger.info(f"[+] Coach Deleted With Id ---> {coach.id} And Email ---> {coach.email}")

    def get_coach(self, coach_id: int):
        logger.info(f"[+] Fetching Coach With Id ---> {coach_id}")
        return self.db.query(Coach).filter(Coach.id == coach_id).first()

    def get_coach_metrics(self, coach_id: int):
        logger.info(f"[+] Fetching Coach Metrics With Id ---> {coach_id}")
        return self.db.query(CoachMetrics).filter(CoachMetrics.coach_id == coach_id).first()

    def get_coach_by_email(self, email: str):
        logger.info(f"[+] Fetching Coach With Email --> {email}")
        return self.db.query(Coach).filter(Coach.email == email).first()

    def get_coach_user(self, coach_id: int):
        logger.info(f"[+] Fetching Coach With Id ---> {coach_id}")

        my_users = (
            self.db.query(User)
            .join(Take, User.id == Take.user_id)
            .join(WorkoutPlan, WorkoutPlan.id == Take.workout_plan_id)
            .join(Present, Present.workout_plan_id == WorkoutPlan.id)
            .filter(Present.coach_id == coach_id)
            .all()
        )
        return my_users

    def get_coach_user_meal_request(self, coach_id: int):
        logger.info(f"[+] Fetching Coach With Id ---> {coach_id}")

        # my_users = (
        #     self.db.query(User)
        #     .join(UserRequestMeal, User.id == UserRequestMeal.user_id)
        #     .join(UserMeal, UserMeal.id == UserRequestMeal.user_meal_id)
        #     .join(Take, User.id == Take.user_id)
        #     .join(WorkoutPlan, WorkoutPlan.id == Take.workout_plan_id)
        #     .join(Present, Present.workout_plan_id == WorkoutPlan.id)
        #     .filter(Present.coach_id == coach_id)
        #     .all()
        # )

        my_users = (
            self.db.query(User)
            .join(UserRequestMeal, User.id == UserRequestMeal.user_id)
            .join(UserMeal, UserMeal.id == UserRequestMeal.user_meal_id)
            .join(Take, User.id == Take.user_id)
            .join(WorkoutPlan, WorkoutPlan.id == Take.workout_plan_id)
            .join(Present, Present.workout_plan_id == WorkoutPlan.id)
            .outerjoin(UserMealMealSupplement, UserMeal.id == UserMealMealSupplement.user_meal_id)
            .filter(Present.coach_id == coach_id)
            .filter(UserMealMealSupplement.user_meal_id.is_(None))
            .all()
        )

        # my_users = (
        #     self.db.query(User)
        #     .join(UserRequestMeal, User.id == UserRequestMeal.user_id)
        #     .join(UserMeal, UserMeal.id == UserRequestMeal.user_meal_id)
        #     .join(Take, User.id == Take.user_id)
        #     .join(WorkoutPlan, WorkoutPlan.id == Take.workout_plan_id)
        #     .join(Present, Present.workout_plan_id == WorkoutPlan.id)
        #     .filter(Present.coach_id == coach_id)
        #     .filter(
        #         ~self.db.query(UserMealMealSupplement)
        #         .filter(UserMealMealSupplement.user_meal_id == UserMeal.id)
        #         .exists()
        #     )
        #     .all()
        # )

        return my_users

    def get_user_meal_meal_supplement(self):
        logger.info("[+] Fetching All User Meal Meal Supplement")
        return self.db.query(UserMealMealSupplement).all()

    def create_meal_supplement(self, meal_supplement: MealSupplement):
        self.db.add(meal_supplement)
        self.db.commit()
        self.db.refresh(meal_supplement)
        logger.info(f"[+] Meal Supplement Created With Meal Id ---> {meal_supplement.id}")
        return meal_supplement

    def create_user_meal_meal_supplement(self, user_meal_meal_supplement: UserMealMealSupplement):
        self.db.add(user_meal_meal_supplement)
        self.db.commit()
        self.db.refresh(user_meal_meal_supplement)
        logger.info(
            f"[+] User Meal Meal Supplement Created For User With Id ---> {user_meal_meal_supplement.user_meal_id}")
        return user_meal_meal_supplement

    def create_work_out_plan_meal_supplement(self, workout_plan_meal_supplement: WorkoutPlanMealSupplement):
        self.db.add(workout_plan_meal_supplement)
        self.db.commit()
        self.db.refresh(workout_plan_meal_supplement)
        logger.info(
            f"[+] Workout Plan Meal Supplement Created With Workout Plan Id ---> {workout_plan_meal_supplement.workout_plan_id}")
        return workout_plan_meal_supplement

    def get_is_answered_requested_meal(self, user_meal_id: int):
        is_answered = (
            self.db.query(UserMealMealSupplement)
            .filter(UserMealMealSupplement.user_meal_id == user_meal_id)
            .first()
        )
        return is_answered

    def get_coach_user_exercise_request(self, coach_id: int):
        logger.info(f"[+] Fetching Coach With Id ---> {coach_id}")

        my_users = (
            self.db.query(User)
            .join(UserRequestExercise, User.id == UserRequestExercise.user_id)
            .join(UserExercise, UserExercise.id == UserRequestExercise.user_exercise_id)
            .join(Take, User.id == Take.user_id)
            .join(WorkoutPlan, WorkoutPlan.id == Take.workout_plan_id)
            .join(Present, Present.workout_plan_id == WorkoutPlan.id)
            .outerjoin(UserExerciseExercise, UserExercise.id == UserExerciseExercise.user_exercise_id)
            .filter(Present.coach_id == coach_id)
            .filter(UserExerciseExercise.user_exercise_id.is_(None))
            .all()
        )
        return my_users

    def get_is_answered_requested_exercise(self, user_exercise_id: int):
        is_answered = (
            self.db.query(UserExerciseExercise)
            .filter(UserExerciseExercise.user_exercise_id == user_exercise_id)
            .first()
        )
        return is_answered

    def create_exercise(self, exercise: Exercise):
        self.db.add(exercise)
        self.db.commit()
        self.db.refresh(exercise)
        logger.info(f"[+] Exercise Created With Id ---> {exercise.id}")
        return exercise

    def create_user_exercise_exercise(self, user_exercise_exercise: UserExerciseExercise):
        self.db.add(user_exercise_exercise)
        self.db.commit()
        self.db.refresh(user_exercise_exercise)
        logger.info(f"[+] User Exercise Exercise Created")
        return user_exercise_exercise

    def create_workout_plan_exercise(self, workout_plan_exercise: WorkoutPlanExercise):
        self.db.add(workout_plan_exercise)
        self.db.commit()
        self.db.refresh(workout_plan_exercise)
        logger.info(f"[+] Workout Plan Exercise Created")
        return workout_plan_exercise

    def create_workout_plan(self, workout_plan: WorkoutPlan):
        self.db.add(workout_plan)
        self.db.commit()
        self.db.refresh(workout_plan)
        logger.info(f"[+] Workout Plan Created")
        return workout_plan

    def create_present(self, present: Present):
        self.db.add(present)
        self.db.commit()
        self.db.refresh(present)
        logger.info(f"[+] Present Created")
        return present

    def check_if_workout_plan_exists(self, coach_id: int):
        logger.info(f"[+] Checking If Workout Plan Exists for Coach With Id ---> {coach_id}")
        return self.db.query(Present).filter(Present.coach_id == coach_id).first()

    def coach_get_coach_plan_price(self, coach_id: int):
        logger.info(f"[+] Fetching Coach Plan Price Associated With Coach ---> {coach_id}")

        coach_plan_price = (
            self.db.query(CoachPlanPrice)
            .filter(CoachPlanPrice.coach_id == coach_id)
            .first()
        )

        return coach_plan_price

    def coach_create_coach_plan_price(self, coach_plan_price_model: CoachPlanPrice):
        self.db.add(coach_plan_price_model)
        self.db.commit()
        self.db.refresh(coach_plan_price_model)
        logger.info(f"[+] Coach Plan Price Created")
        return coach_plan_price_model

    def coach_update_coach_plan_price(self, coach_id: int, updated_coach_plan_price: Dict):
        coach_plan_price_query = self.db.query(CoachPlanPrice).filter(CoachPlanPrice.coach_id == coach_id)
        db_coach_plan_price = coach_plan_price_query.first()
        coach_plan_price_query.filter(CoachPlanPrice.coach_id == coach_id).update(
            updated_coach_plan_price, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_coach_plan_price)
        logger.info(f"[+] Coach Plan Price For Coach With Id ---> {coach_id} Updated")
        return db_coach_plan_price

    def coach_get_verified_gym_plan_price(self, coach_id: int, gym_id: int):
        logger.info(f"[+] Fetching Verified Gym Plan Price For Coach With Id ---> {coach_id}")

        verified_gym_plan_price = (
            self.db.query(GymPlanPrice)
            .join(Gym, GymPlanPrice.gym_id == Gym.id)
            .filter(Gym.owner_id == coach_id)
            .filter(Gym.id == gym_id)
            .filter(Gym.verification_status == "verified")
            .all()
        )

        return verified_gym_plan_price

    def coach_get_his_gym_info(self, coach_id: int):
        logger.info(f"[+] Fetching Verified Gym For Coach With Id ---> {coach_id}")

        verified_gym_info = (
            self.db.query(Gym)
            .filter(Gym.owner_id == coach_id)
            .filter(Gym.verification_status == "verified")
            .all()
        )

        return verified_gym_info

    def get_gym_info(self, gym_id: int):
        logger.info("[+] Fetching Gym Owner For Gym With Id ---> {gym_id}")
        gym_info = (
            self.db.query(Gym)
            .filter(Gym.id == gym_id)
            .filter(Gym.verification_status == "verified")
            .first()
        )
        return gym_info

    def coach_create_verified_gym_plan_price(self, verified_gym_plan_price: GymPlanPrice):
        logger.info(f"[+] Creating New Gym Plan Price for gym")
        self.db.add(verified_gym_plan_price)
        self.db.commit()
        self.db.refresh(verified_gym_plan_price)
        logger.info(f"[+] Gym Plan Price Created")
        return verified_gym_plan_price

    def check_plan_price_exists_and_valid(self, plan_price_id: int):
        logger.info("[+] Checking If Gym Plan Price Exists And Is Valid")

        plan_price = (
            self.db.query(GymPlanPrice)
            .filter(GymPlanPrice.id == plan_price_id)
            .first()
        )

        return plan_price

    def coach_delete_gym_plan_price(self, plan_price_id: int):
        logger.info(f"[+] Deleting Gym Plan Price With Id ---> {plan_price_id}")
        gym_plan_price_query = self.db.query(GymPlanPrice).filter(GymPlanPrice.id == plan_price_id)
        db_gym_plan_price = gym_plan_price_query.first()
        gym_plan_price_query.delete(synchronize_session=False)
        self.db.commit()
        logger.info(f"[+] Gym Plan Price Deleted With Id ---> {plan_price_id}")
        return db_gym_plan_price

    def coach_update_gym_plan_price(self, plan_price_id: int, updated_gym_plan_price: Dict):
        logger.info("[+] Updating Gym Plan Price With Id ---> {plan_price_id}")
        gym_plan_price_query = self.db.query(GymPlanPrice).filter(GymPlanPrice.id == plan_price_id)
        db_gym_plan_price = gym_plan_price_query.first()
        gym_plan_price_query.filter(GymPlanPrice.id == plan_price_id).update(
            updated_gym_plan_price, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_gym_plan_price)
        logger.info(f"[+] Gym Plan Price Updated With Id ---> {plan_price_id}")
        return db_gym_plan_price
