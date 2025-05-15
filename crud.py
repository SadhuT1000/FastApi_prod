import asyncio

from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, User, Profile, Post
from typing import Union


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(
    session: AsyncSession, username: str
) -> Union[User, None]:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: Union[User, None] = result.scalar_one_or_none()
    user = await session.scalar(stmt)
    print("found user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: Union[str, None] = None,
    last_name: Union[str, None] = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *posts_titles: str,
) -> list[Post]:
    posts = [
        Post(
            title=title,
            user_id=user_id,
        )
        for title in posts_titles
    ]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(session: AsyncSession):
    stmt = (
        select(User)
        .options(
            # joinedload(User.posts),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    for user in users:
        print(("**" * 10))
        print(user)
        for post in user.posts:
            print("-", post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    for post in posts:
        print("post", post)
        print("author", post.user)


async def get_users_with_posts_and_profiles(session: AsyncSession):
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    for user in users:
        print(("**" * 10))
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(joinedload(Profile.user).selectinload(User.posts))
        .where(User.username == "Tom")
        .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(("**" * 10))
        print(profile.first_name, profile.user)
        print("-", profile.user.posts)


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="Elly")
        # await create_user(session=session, username="Smith")
        # user_smith = await get_user_by_username(session=session, username="Smith")
        # user_tom = await get_user_by_username(session=session, username="Tom")
        # await create_user_profile(
        #     session=session,
        #     user_id=user_smith.id,
        #     first_name="smith",
        #     last_name="trum",
        # )
        # await create_user_profile(
        #     session=session,
        #     user_id=user_tom.id,
        #     first_name="Tommy",
        #     last_name="Last",
        # )
        # await show_users_profiles(session=session)
        # await create_posts(
        #     session,
        #     user_tom.id,
        #     "Spark",
        #     "Airflow",
        # )
        # await create_posts(
        #     session,
        #     user_smith.id,
        #     "Fastapi",
        #     "Flask",
        # )
        # await get_users_with_posts(session=session)
        # await get_posts_with_authors(session=session)
        # await get_users_with_posts_and_profiles(session=session)
        await get_profiles_with_users_and_users_with_posts(session=session)


if __name__ == "__main__":
    asyncio.run(main())
