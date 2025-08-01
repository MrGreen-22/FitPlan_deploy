from sqlalchemy import (Column, Integer, String, Text, TIMESTAMP, func, Sequence, ForeignKey, Numeric, Boolean,
                        DECIMAL, CheckConstraint, PrimaryKeyConstraint)
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(255), nullable=False)
    user_name = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True)
    gender = Column(String(10))
    date_of_birth = Column(String(15))
    image = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now())
    is_verified = Column(Boolean, default=False)

    metrics = relationship("UserMetrics", back_populates="user", uselist=False)
    user_transactions = relationship("UserTransactionLog", back_populates="user")
    # workout_plans = relationship('WorkoutPlan', secondary='take', back_populates='user')
    takes = relationship('Take', back_populates='user')
    user_requests = relationship("UserRequestExercise", back_populates="user")
    user_request_meals = relationship("UserRequestMeal", back_populates="user")
    gym_comments = relationship("GymComment", back_populates="user", cascade="all, delete-orphan")
    gym_registrations = relationship("UserGymRegistration", back_populates="user", cascade="all, delete-orphan")

    coach_comments = relationship("CoachComment", back_populates="user", cascade="all, delete-orphan")


class UserMetrics(Base):
    __tablename__ = 'user_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    height = Column(Numeric(5, 2))
    weight = Column(Numeric(5, 2))
    waist = Column(Numeric(5, 2))
    injuries = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="metrics")


class Coach(Base):
    __tablename__ = "coach"

    id = Column(Integer, Sequence("coach_id_seq"), primary_key=True)
    password = Column(String(255), nullable=False)
    user_name = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    gender = Column(String(10))
    status = Column(Boolean, default=False)
    date_of_birth = Column(String(15))
    image = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now())
    is_verified = Column(Boolean, default=False)
    verification_status = Column(String(50), default="pending")

    metrics = relationship("CoachMetrics", back_populates="coach", uselist=False)
    present = relationship('Present', back_populates='coach')
    gyms = relationship("CoachGym", back_populates="coach")

    comments = relationship("CoachComment", back_populates="coach", cascade="all, delete-orphan")
    plan_price = relationship("CoachPlanPrice", back_populates="coach", uselist=False)


class CoachMetrics(Base):
    __tablename__ = 'coach_metrics'

    id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, ForeignKey('coach.id', ondelete='CASCADE'), unique=True)
    height = Column(Numeric(5, 2))
    weight = Column(Numeric(5, 2))
    specialization = Column(String(255))
    biography = Column(Text)

    rating = Column(Integer, default=0)
    coaching_id = Column(String(100), nullable=False)
    coaching_card_image = Column(Text)

    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint('rating BETWEEN 0 AND 5', name='check_coach_rating_range'),
    )

    # Relationship with Coach
    coach = relationship("Coach", back_populates="metrics")


class UserDuplicates(Base):
    __tablename__ = 'user_duplicates'
    id = Column(Integer, Sequence('user_duplicates_id_seq'), primary_key=True)
    user_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)


class TransactionLog(Base):
    __tablename__ = 'transaction_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    reason = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    date = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user_transaction = relationship("UserTransactionLog", back_populates="transaction")


class UserTransactionLog(Base):
    __tablename__ = 'user_transaction_log'

    transaction_id = Column(Integer, ForeignKey('transaction_log.id', ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

    transaction = relationship("TransactionLog", back_populates="user_transaction")
    user = relationship("User", back_populates="user_transactions")


class WorkoutPlan(Base):
    __tablename__ = 'workout_plan'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    duration_month = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    # users = relationship('User', secondary='take', back_populates='workout_plans')
    # coach = relationship('Coach', secondary='present', back_populates='workout_plans')
    takes = relationship('Take', back_populates='workout_plan')
    present = relationship('Present', back_populates='workout_plan')
    exercises = relationship("WorkoutPlanExercise", back_populates="workout_plan")
    workout_plan_meal_supplements = relationship("WorkoutPlanMealSupplement", back_populates="workout_plan")


class Take(Base):
    __tablename__ = 'take'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    workout_plan_id = Column(Integer, ForeignKey('workout_plan.id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    user = relationship('User', back_populates='takes')
    workout_plan = relationship('WorkoutPlan', back_populates='takes')


class Present(Base):
    __tablename__ = 'present'

    coach_id = Column(Integer, ForeignKey('coach.id', ondelete='CASCADE'), primary_key=True)
    workout_plan_id = Column(Integer, ForeignKey('workout_plan.id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    coach = relationship('Coach', back_populates='present')
    workout_plan = relationship('WorkoutPlan', back_populates='present')


class UserExercise(Base):
    __tablename__ = 'user_exercise'

    id = Column(Integer, primary_key=True, autoincrement=True)
    weight = Column(DECIMAL(5, 2), nullable=False)
    waist = Column(DECIMAL(5, 2), nullable=False)
    type = Column(String(10), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    image = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp(),
                        nullable=False)

    user_requests = relationship("UserRequestExercise", back_populates="exercise")
    exercise_links = relationship("UserExerciseExercise", back_populates="user_exercise")


class UserRequestExercise(Base):
    __tablename__ = 'user_request_exercise'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user_exercise_id = Column(Integer, ForeignKey('user_exercise.id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    user = relationship("User", back_populates="user_requests")
    exercise = relationship("UserExercise", back_populates="user_requests")


class Exercise(Base):
    __tablename__ = 'exercise'

    id = Column(Integer, primary_key=True, autoincrement=True)
    day = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    set = Column(String(100), nullable=False)
    expire_time = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp(),
                        nullable=False)

    # Relationship to workout_plan_exercise
    workout_plans = relationship("WorkoutPlanExercise", back_populates="exercise")
    user_exercise_links = relationship("UserExerciseExercise", back_populates="exercise")


class WorkoutPlanExercise(Base):
    __tablename__ = 'workout_plan_exercise'

    exercise_id = Column(Integer, ForeignKey('exercise.id', ondelete='CASCADE'), primary_key=True)
    workout_plan_id = Column(Integer, ForeignKey('workout_plan.id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    exercise = relationship("Exercise", back_populates="workout_plans")
    workout_plan = relationship("WorkoutPlan", back_populates="exercises")


class UserExerciseExercise(Base):
    __tablename__ = 'user_exercise_exercise'

    exercise_id = Column(Integer, ForeignKey('exercise.id', ondelete='CASCADE'), primary_key=True)
    user_exercise_id = Column(Integer, ForeignKey('user_exercise.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    exercise = relationship("Exercise", back_populates="user_exercise_links")
    user_exercise = relationship("UserExercise", back_populates="exercise_links")


class UserMeal(Base):
    __tablename__ = "user_meal"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    weight = Column(DECIMAL(5, 2), nullable=False)
    waist = Column(DECIMAL(5, 2), nullable=False)
    type = Column(String(10), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    image = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user_requests = relationship("UserRequestMeal", back_populates="user_meal")
    user_meal_meal_supplement = relationship("UserMealMealSupplement", back_populates="user_meal")


class UserRequestMeal(Base):
    __tablename__ = "user_request_meal"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user_meal_id = Column(Integer, ForeignKey("user_meal.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="user_request_meals")
    user_meal = relationship("UserMeal", back_populates="user_requests")


class MealSupplement(Base):
    __tablename__ = "meal_supplement"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    breakfast = Column(Text, nullable=True)
    lunch = Column(Text, nullable=True)
    dinner = Column(Text, nullable=True)
    supplement = Column(Text, nullable=True)
    expire_time = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    workout_plan_meal_supplements = relationship("WorkoutPlanMealSupplement", back_populates="meal_supplement")
    user_meal_meal_supplements = relationship("UserMealMealSupplement", back_populates="meal_supplement")


class WorkoutPlanMealSupplement(Base):
    __tablename__ = "workout_plan_meal_supplement"

    meal_supplement_id = Column(Integer, ForeignKey("meal_supplement.id", ondelete="CASCADE"), primary_key=True)
    workout_plan_id = Column(Integer, ForeignKey("workout_plan.id", ondelete="CASCADE"), primary_key=True)

    # Relationships
    meal_supplement = relationship("MealSupplement", back_populates="workout_plan_meal_supplements")
    workout_plan = relationship("WorkoutPlan", back_populates="workout_plan_meal_supplements")


class UserMealMealSupplement(Base):
    __tablename__ = "user_meal_meal_supplement"

    meal_supplement_id = Column(Integer, ForeignKey("meal_supplement.id", ondelete="CASCADE"), primary_key=True)
    user_meal_id = Column(Integer, ForeignKey("user_meal.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Relationships
    meal_supplement = relationship("MealSupplement", back_populates="user_meal_meal_supplements")
    user_meal = relationship("UserMeal", back_populates="user_meal_meal_supplement")


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, Sequence("admin_id_seq"), primary_key=True)
    password = Column(String(255), nullable=False)
    user_name = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    gender = Column(String(10))
    date_of_birth = Column(String(15))
    image = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now())
    is_verified = Column(Boolean, default=False)


# ********************************************************************************

class Gym(Base):
    __tablename__ = "gym"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("coach.id", ondelete="CASCADE"), nullable=False)

    name = Column(String(255), nullable=False)
    license_number = Column(String(100), nullable=False)
    license_image = Column(Text, nullable=True)
    location = Column(Text, nullable=True)
    image = Column(Text, nullable=True)
    sport_facilities = Column(Text, nullable=True)
    welfare_facilities = Column(Text, nullable=True)

    rating = Column(Integer, default=0)
    verification_status = Column(String(50), default="pending")

    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint('rating BETWEEN 0 AND 5', name='check_rating_range'),
    )

    coaches = relationship("CoachGym", back_populates="gym")
    plan_price = relationship("GymPlanPrice", back_populates="gym")
    comments = relationship("GymComment", back_populates="gym", cascade="all, delete-orphan")
    user_registrations = relationship("UserGymRegistration", back_populates="gym", cascade="all, delete-orphan")


class CoachGym(Base):
    __tablename__ = "coach_gym"

    coach_id = Column(Integer, ForeignKey("coach.id", ondelete="CASCADE"), nullable=False)
    gym_id = Column(Integer, ForeignKey("gym.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('coach_id', 'gym_id'),
    )

    coach = relationship("Coach", back_populates="gyms")
    gym = relationship("Gym", back_populates="coaches")


class GymPlanPrice(Base):
    __tablename__ = "gym_plan_price"

    id = Column(Integer, primary_key=True, index=True)
    gym_id = Column(Integer, ForeignKey("gym.id", ondelete="CASCADE"), nullable=False)

    session_counts = Column(Integer, nullable=False)
    duration_days = Column(Integer, nullable=False)
    is_vip = Column(Boolean, default=False)
    price = Column(Integer, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    gym = relationship("Gym", back_populates="plan_price", uselist=False)

    __table_args__ = (
        CheckConstraint('session_counts >= 0', name='check_session_counts_positive'),
        CheckConstraint('duration_days >= 0', name='check_duration_days_positive'),
        CheckConstraint('price >= 0', name='check_price_positive'),
    )


class GymComment(Base):
    __tablename__ = "gym_comment"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    gym_id = Column(Integer, ForeignKey("gym.id", ondelete="CASCADE"), nullable=False)

    comment = Column(Text, nullable=True)
    rating = Column(Integer, default=0)
    date = Column(String(100), nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="gym_comments")
    gym = relationship("Gym", back_populates="comments")

    __table_args__ = (
        CheckConstraint('rating BETWEEN 0 AND 5', name='check_gym_comment_rating_range'),
    )


class UserGymRegistration(Base):
    __tablename__ = "user_gym_registration"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    gym_id = Column(Integer, ForeignKey("gym.id", ondelete="CASCADE"), nullable=False)

    registered_sessions = Column(Integer, default=0)
    registered_days = Column(Integer, default=0)
    is_vip = Column(Boolean, default=False)
    remaining_sessions = Column(Integer, default=0)
    remaining_days = Column(Integer, default=0)
    is_expired = Column(Boolean, default=False)
    date = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="gym_registrations")
    gym = relationship("Gym", back_populates="user_registrations")


class CoachComment(Base):
    __tablename__ = "coach_comment"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    coach_id = Column(Integer, ForeignKey("coach.id", ondelete="CASCADE"), nullable=False)

    comment = Column(Text, nullable=True)
    rating = Column(Integer, default=0)
    date = Column(String(100), nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="coach_comments")
    coach = relationship("Coach", back_populates="comments")

    __table_args__ = (
        CheckConstraint('rating BETWEEN 0 AND 5', name='check_gym_comment_rating_range'),
    )


class CoachPlanPrice(Base):
    __tablename__ = "coach_plan_price"

    id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, ForeignKey("coach.id", ondelete="CASCADE"), nullable=False, unique=True)

    exercise_price = Column(Integer, nullable=False)
    meal_price = Column(Integer, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    coach = relationship("Coach", back_populates="plan_price", uselist=False)

    __table_args__ = (
        CheckConstraint('exercise_price >= 0', name='check_exercise_price_positive'),
        CheckConstraint('meal_price >= 0', name='check_meal_price_positive'),
    )
