# WeChat Exporter (mac)

Minimal, offline-friendly tools to clean and render text exported from the macOS WeChat client.

## Prepare `raw_dump.txt` with Hammerspoon

1. Install [Hammerspoon](https://www.hammerspoon.org/).
2. Create `~/.hammerspoon/wechat_dump.lua` with a hotkey that OCRs the visible WeChat window and appends the text to a file:

   ```lua
   local destination = os.getenv("HOME") .. "/Desktop/raw_dump.txt"

   -- Press Ctrl+Alt+Cmd+D to OCR the visible WeChat chat area and append the text.
   hs.hotkey.bind({"ctrl", "alt", "cmd"}, "D", function()
     local win = hs.window.focusedWindow()
     if not win or not string.find(win:application():name(), "WeChat") then
       hs.alert.show("Focus the WeChat window first")
       return
     end

     local img = win:snapshot()
     local text = hs.ocr.imageToText(img)
     if text and string.len(text) > 0 then
       local file = io.open(destination, "a")
       file:write(text)
       file:write("\n\n") -- blank line separates screens
       file:close()
       hs.alert.show("Captured screen to raw_dump.txt")
     else
       hs.alert.show("No text detected")
     end
   end)
   ```

3. Reload Hammerspoon and press the hotkey while scrolling through the conversation in WeChat. Each press captures the current screen and appends it to `raw_dump.txt`.

> The exporter does **not** read the WeChat database or call external APIs; it only processes the text you capture.

## CLI usage

```bash
python3 -m wechat_exporter.cli dedup --in raw_dump.txt --out deduped.txt
python3 -m wechat_exporter.cli render --in deduped.txt --format md --out chat.md
```

### Command details

- `dedup`: removes duplicate screens in `raw_dump.txt` based on their text content.
- `render`: outputs either raw text (`txt`) or Markdown (`md`). Markdown output wraps the entire conversation in a fenced code block to keep formatting intact.

## Samples

`samples/raw_dump_example.txt` demonstrates the expected raw input (with repeated screens). Run the CLI commands above against it to see the deduplication and rendering flow.
