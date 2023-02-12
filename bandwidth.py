#!/bin/python3
import psutil
import time
import curses
import atexit

def get_stats():
    results = {}
    stats = psutil.net_io_counters(pernic=True)
    for ifc in stats:
        results[ifc] = { "sent" : stats[ifc].bytes_sent, "recv" : stats[ifc].bytes_recv } 
    return results

def on_exit():
    curses.endwin()
    print("Done!")

def start():
    curses.init_pair(91, curses.COLOR_BLACK, curses.COLOR_WHITE);
    try:
        start=last=get_stats()
        time.sleep(1)
        data_txt = "{0:10} {1:>9} {2:>9} {3:>9} {4:>9}"
        while True:
            win.clear()
            win.addstr(0,0, data_txt.format("ifc", "sec_sent", "sec_recv", "tot_sent", "tot_recv"), curses.color_pair(91))
            stats = get_stats()
            row = 1
            for ifc in stats:
                sec_sent = stats[ifc]["sent"]-last[ifc]["sent"]
                sec_recv = stats[ifc]["recv"]-last[ifc]["recv"]
                tot_sent = stats[ifc]["sent"]-start[ifc]["sent"]
                tot_recv = stats[ifc]["recv"]-start[ifc]["recv"]
                win.addstr(row,0,data_txt.format(ifc, sec_sent, sec_recv, tot_sent, tot_recv)) 
                row += 1
            win.refresh()
            last = stats
            time.sleep(1)
    except KeyboardInterrupt:
        print("done")


# print(stats)
atexit.register(on_exit)
win = curses.initscr()
curses.start_color()
curses.savetty()
start()

