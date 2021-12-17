--[[
SOURCE_ https://github.com/mpv-player/mpv/blob/master/TOOLS/lua/ontop-playback.lua
COMMIT_ 20150323 c48de9e

使用此脚本后 --ontop 仅在播放状态时启用置顶，暂停自动取消置顶
同功能的 on_top_only_while_playing.lua 脚本存在以暂停状态启动mpv时无法识别的问题
--]]

local was_ontop = false

mp.observe_property("pause", "bool", function(name, value)
    local ontop = mp.get_property_native("ontop")
    if value then
        if ontop then
            mp.set_property_native("ontop", false)
            was_ontop = true
        end
    else
        if was_ontop and not ontop then
            mp.set_property_native("ontop", true)
        end
        was_ontop = false
    end
end)
