from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Asset, MaintenanceLog

async def get_asset_by_tag(db: AsyncSession, asset_tag: str):
    result = await db.execute(select(Asset).where(Asset.asset_tag == asset_tag))
    return result.scalars().first()

async def get_assets_under_maintenance(db: AsyncSession):
    result = await db.execute(select(Asset).where(Asset.status == "Under Maintenance"))
    return result.scalars().all()
