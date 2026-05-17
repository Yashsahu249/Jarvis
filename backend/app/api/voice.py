import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, File, UploadFile, Form, HTTPException
from loguru import logger
from app.models.schemas import VoiceTranscribeResponse, VoiceSynthesizeRequest, VoiceSynthesizeResponse
from app.services.voice_service import voice_service

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/transcribe", response_model=VoiceTranscribeResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = Form(None),
    model_size: str = Form(None),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    temp_path = f"/tmp/jarvis_audio_{id(file)}"
    try:
        content = await file.read()
        with open(temp_path, "wb") as f:
            f.write(content)

        result = await voice_service.transcribe(temp_path, language=language, model_size=model_size)
        return VoiceTranscribeResponse(
            text=result["text"],
            segments=result.get("segments"),
            duration=result.get("duration"),
            language=result.get("language"),
        )
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        import os
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@router.post("/synthesize", response_model=VoiceSynthesizeResponse)
async def synthesize_speech(req: VoiceSynthesizeRequest):
    try:
        result = await voice_service.synthesize(text=req.text, voice=req.voice, speed=req.speed)
        return VoiceSynthesizeResponse(
            audio_path=result["audio_path"],
            duration=result.get("duration"),
        )
    except Exception as e:
        logger.error(f"Synthesis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/stream")
async def voice_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                text = payload.get("text", "")
            except json.JSONDecodeError:
                text = data

            if not text:
                continue

            async for audio_chunk in voice_service.stream_audio(text):
                await websocket.send_bytes(audio_chunk)

            await websocket.send_json({"type": "done", "text": text})
    except WebSocketDisconnect:
        logger.info("Voice stream client disconnected")
    except Exception as e:
        logger.error(f"Voice stream error: {e}")
        try:
            await websocket.send_json({"type": "error", "error": str(e)})
        except Exception:
            pass
