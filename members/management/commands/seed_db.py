from django.core.management.base import BaseCommand
from faker import Faker
import random
from decimal import Decimal

from members.models import Branch, Plan, MemberShip, MemberShipUsage
from users.models import User, UserInformation, TrainerProfile, MemberTrainer

fake = Faker()


class Command(BaseCommand):
    help = "Seed database with realistic gym data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")

        MemberTrainer.objects.all().delete()
        MemberShipUsage.objects.all().delete()
        MemberShip.objects.all().delete()
        TrainerProfile.objects.all().delete()
        UserInformation.objects.all().delete()
        Plan.objects.all().delete()
        Branch.objects.all().delete()
        User.objects.all().delete()

        fake.unique.clear()

        # =====================
        # 1. BRANCHES
        # =====================
        cities = [
            "tanta","cairo","alexandria","mansura","suez",
            "north_sinai","london","berlin","barcelona","stockholm"
        ]

        branches = [
            Branch.objects.create(
                branch_name=f"Branch_{i+1}",
                city=cities[i]
            )
            for i in range(10)
        ]

        self.stdout.write("Branches created")

        # =====================
        # 2. PLANS
        # =====================
        plans = []

        for branch in branches:
            for i in range(random.randint(4, 7)):
                plans.append(
                    Plan(
                        branch=branch,
                        plan_name=f"{branch.branch_name}_Plan_{i+1}",
                        price=Decimal(random.randint(500, 3000)),
                        duration=random.choice([
                            "one_month",
                            "three_months",
                            "six_months",
                            "twelve_months"
                        ]),
                        number_of_sessions=random.randint(8, 40),
                        number_of_spa_sessions=random.randint(0, 10),
                        number_of_suana_sessions=random.randint(0, 10),
                        number_of_jacuzzi_sessions=random.randint(0, 10),
                    )
                )

        Plan.objects.bulk_create(plans)
        self.stdout.write("Plans created")

        plans = list(Plan.objects.all())

        # =====================
        # 3. USERS
        # =====================
        users = []
        user_info = []
        trainer_profiles_data = []
        member_list = []

        user_id_counter = 1

        for branch in branches:
            self.stdout.write(f"Creating users for {branch.branch_name}...")

            # ADMINS
            for _ in range(random.randint(5, 15)):
                users.append(User(
                    username=f"admin_{user_id_counter}",
                    email=f"admin_{user_id_counter}@mail.com",
                    role="admin",
                    is_staff=True,
                    is_active=True
                ))
                user_id_counter += 1

            # TRAINERS
            for _ in range(random.randint(10, 20)):
                users.append(User(
                    username=f"trainer_{user_id_counter}",
                    email=f"trainer_{user_id_counter}@mail.com",
                    role="trainer",
                    is_staff=False,
                    is_active=True
                ))
                user_id_counter += 1

            # MEMBERS
            for _ in range(random.randint(70, 110)):
                u = User(
                    username=f"member_{user_id_counter}",
                    email=f"member_{user_id_counter}@mail.com",
                    role="member",
                    is_staff=False,
                    is_active=True
                )
                users.append(u)
                member_list.append(u)
                user_id_counter += 1

        User.objects.bulk_create(users)
        self.stdout.write("Users created")

        users = list(User.objects.all())

        # =====================
        # 4. USER INFO
        # =====================
        for i, u in enumerate(users):
            user_info.append(
                UserInformation(
                    user=u,
                    branch=random.choice(branches),
                    phone_number=f"0100{i:06d}",
                    gender=random.choice(["male", "female"]),
                    date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=60),
                )
            )

        UserInformation.objects.bulk_create(user_info)
        self.stdout.write("UserInformation created")

        # =====================
        # 5. TRAINER PROFILES (FIXED LOGIC)
        # =====================
        trainer_users = [u for u in users if u.role == "trainer"]

        trainer_profiles = []
        active_trainers = []

        for u in trainer_users:
            is_fired = random.random() < 0.15  # 15% fired trainers

            profile = TrainerProfile(
                user=u,
                is_fired=is_fired,
                is_active=not is_fired,
                salary=Decimal(random.randint(3000, 15000)),
                years_of_experience=random.randint(0, 15),
            )

            trainer_profiles.append(profile)

            if not is_fired:
                active_trainers.append(u)

        TrainerProfile.objects.bulk_create(trainer_profiles)
        self.stdout.write("Trainer profiles created")

        # =====================
        # 6. MEMBERSHIPS
        # =====================
        memberships = []
        usage = []

        for member in member_list:
            plan = random.choice(plans)

            m = MemberShip.objects.create(
                member=member,
                plan=plan,
                amount_paid=plan.price,
                status="active"
            )

            usage.append(
                MemberShipUsage(
                    membership=m,
                    sessions_used=random.randint(0, 10),
                    spa_sessions_used=random.randint(0, 5),
                    suana_sessions_used=random.randint(0, 5),
                    jacuzzi_sessions_used=random.randint(0, 5),
                )
            )

        MemberShipUsage.objects.bulk_create(usage)
        self.stdout.write("Memberships created")

        # =====================
        # 7. MEMBER-TRAINER (FIXED: ONLY ACTIVE TRAINERS)
        # =====================
        assignments = []

        for member in member_list:
            if not active_trainers:
                continue

            assignments.append(
                MemberTrainer(
                    member=member,
                    trainer=random.choice(active_trainers),
                    is_active=True
                )
            )

        MemberTrainer.objects.bulk_create(assignments)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))