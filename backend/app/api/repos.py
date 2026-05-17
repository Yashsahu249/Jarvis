from fastapi import APIRouter, HTTPException, Query
from loguru import logger
from app.models.schemas import RepoInfo, RepoFile, RepoCloneRequest, RepoAnalyzeRequest, RepoSearchRequest
from app.services.repo_service import repo_service

router = APIRouter(prefix="/repos", tags=["repos"])


@router.post("/clone", response_model=RepoInfo)
async def clone_repository(req: RepoCloneRequest):
    try:
        result = await repo_service.clone(url=req.url, name=req.name, branch=req.branch, depth=req.depth)
        return RepoInfo(**result)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Clone error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=list[RepoInfo])
async def list_repos():
    repos = repo_service.list_repos()
    return [RepoInfo(**r) for r in repos]


@router.get("/{repo_id}/structure", response_model=list[RepoFile])
async def get_repo_structure(repo_id: str, path: str = Query("", description="Subdirectory path")):
    try:
        items = repo_service.get_structure(repo_id, path=path)
        return [RepoFile(**item) for item in items]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Structure error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{repo_id}/files/{path:path}")
async def get_file_content(repo_id: str, path: str):
    try:
        result = repo_service.get_file(repo_id, path)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"File read error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{repo_id}/analyze")
async def analyze_repository(repo_id: str, req: RepoAnalyzeRequest):
    try:
        result = await repo_service.analyze(
            repo_id=repo_id, task=req.task, files=req.files, context=req.context
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{repo_id}/search")
async def search_repository(repo_id: str, req: RepoSearchRequest):
    try:
        result = await repo_service.search(
            repo_id=repo_id,
            query=req.query,
            file_pattern=req.file_pattern,
            max_results=req.max_results,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{repo_id}")
async def remove_repository(repo_id: str):
    try:
        result = repo_service.remove(repo_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Repo {repo_id} not found")
        return {"status": "removed", "repo_id": repo_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Remove error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
