import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp
import os
import tempfile
import logging

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


BOT_TOKEN = '7596997075:AAHsOxLyIlDfqm99dGClXx8xwBCpQ4D85a8'


async def start(update, context):
    """Sends a welcome message when the user sends /start."""
    await update.message.reply_text("Hello! Send me a TikTok or Instagram video/photo link, and I'll try to download it.")


async def download_and_send_media(update, context):
    """Processes the link sent by the user, downloads media, and sends it back."""
    chat_id = update.message.chat_id
    user_message = update.message.text

    logger.info(f"Received message from {chat_id}: {user_message}")

    if "http://" in user_message or "https://" in user_message:
        # Send initial processing message
        processing_message = await context.bot.send_message(chat_id=chat_id, text="Processing link... Please wait.")

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                    'restrictfilenames': True,
                    'noplaylist': True,
                    'quiet': True,
                    'no_warnings': True,
                    'ignoreerrors': True,
                    # Ensure ffmpeg_location is correctly set
                    # If you copied the 'bin' folder of ffmpeg into D:\API_student\myproject\
                    'ffmpeg_location': os.path.join(os.path.dirname(__file__), 'bin'),
                    # ✅ Removed postprocessors section
                }

                downloaded_filepath = None
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Update feedback message
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=processing_message.message_id,
                        text="Downloading content... Please wait a moment."
                    )
                    info_dict = ydl.extract_info(user_message, download=False)

                    if info_dict:
                        downloaded_filepath = ydl.prepare_filename(info_dict)
                        ydl.download([user_message])
                    else:
                        await context.bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=processing_message.message_id,
                            text="Could not retrieve media information from this link."
                        )
                        logger.warning(f"Could not extract info for: {user_message}")
                        return

                if downloaded_filepath and os.path.exists(downloaded_filepath):
                    file_size_mb = os.path.getsize(downloaded_filepath) / (1024 * 1024)
                    logger.info(f"Downloaded file: {downloaded_filepath}, size: {file_size_mb:.2f} MB")

                    if file_size_mb > 50: # Telegram Bot API limit is usually 50MB
                        await context.bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=processing_message.message_id,
                            text=f"This file is too large ({file_size_mb:.2f} MB). I cannot send it via Telegram."
                        )
                    else:
                        # Update feedback message
                        await context.bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=processing_message.message_id,
                            text="Sending file to Telegram... Please wait."
                        )
                        try:
                            with open(downloaded_filepath, 'rb') as media_file:
                                if downloaded_filepath.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
                                    await context.bot.send_video(chat_id=chat_id, video=media_file,
                                                                 caption="Video downloaded!",
                                                                 read_timeout=30, write_timeout=30) # Add timeout for sending
                                elif downloaded_filepath.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                                    await context.bot.send_photo(chat_id=chat_id, photo=media_file,
                                                                 caption="Photo downloaded!",
                                                                 read_timeout=30, write_timeout=30) # Add timeout for sending
                                else:
                                    await context.bot.send_document(chat_id=chat_id, document=media_file,
                                                                  caption="Media downloaded.",
                                                                  read_timeout=30, write_timeout=30) # Add timeout for sending
                            # Delete the "Sending file" message after successful sending
                            await context.bot.delete_message(chat_id=chat_id, message_id=processing_message.message_id)

                        except Exception as e:
                            logger.error(f"Error opening or sending file {downloaded_filepath}: {e}")
                            await context.bot.edit_message_text(
                                chat_id=chat_id,
                                message_id=processing_message.message_id,
                                text="There was an issue sending this file. It might be corrupted."
                            )

                else:
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=processing_message.message_id,
                        text="There was an issue downloading media from this link. Please try a different link or try again."
                    )
                    logger.error(f"Downloaded file not found or empty: {downloaded_filepath}")

        except yt_dlp.DownloadError as e:
            error_message = str(e)
            if "Unsupported URL" in error_message:
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=processing_message.message_id,
                    text="This link is not supported or has an issue."
                )
            elif "Private video" in error_message or "Login required" in error_message:
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=processing_message.message_id,
                    text="This is a private video or requires login. I cannot download it."
                )
            else:
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=processing_message.message_id,
                    text=f"An error occurred while downloading this link: {error_message}"
                )
            logger.error(f"yt-dlp error for {user_message}: {e}")
        except Exception as e:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=processing_message.message_id,
                text=f"A technical error occurred: {e}"
            )
            logger.exception(f"Unhandled error for {user_message}")
    else:
        await context.bot.send_message(chat_id=chat_id, text="Please send me a link (starting with http/https).")


async def error_handler(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_and_send_media))

    application.add_error_handler(error_handler)

    application.run_polling()
    logger.info("Bot started polling...")


if __name__ == '__main__':
    main()