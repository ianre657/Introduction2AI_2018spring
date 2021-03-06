import copy
from collections import OrderedDict
from collections import deque


from computeTree import Point, ComputeNode, ComputeTree
from computeTree import solution_path, solNode

from util import print_solution

# profiling
import atexit
from time import time
bfs_prof_start_time = 0
bfs_prof_end_time = 0
bfs_prof_execute_time = 0
bfs_prof_node_explored = 0
bfs_prof_depth_reached = 0
bfs_prof_max_queue_size = 0

def bfs_show_profile():
    print('BFS profiling outcome'.center(40,'-'))
    print(' execute time:   {:.4} sec'.format(bfs_prof_execute_time))
    print(' node explored:  {}'.format(bfs_prof_node_explored))
    print(' max tree depth: {}'.format(bfs_prof_depth_reached))
    print(' max queue size: {}'.format(bfs_prof_max_queue_size))
    atexit.unregister(exit_handler)


def exit_handler():
    global bfs_prof_end_time, bfs_prof_execute_time,bfs_prof_start_time
    print("program stopped")
    # profiling
    bfs_prof_end_time = time()
    bfs_prof_execute_time = bfs_prof_end_time - bfs_prof_start_time
    # profiling end
    bfs_show_profile()


def bfs_find_solution(game_tree, show_profiling=False):
    global bfs_prof_max_queue_size
    global bfs_prof_start_time, bfs_prof_end_time,bfs_prof_execute_time
    global bfs_prof_node_explored, bfs_prof_depth_reached

    if show_profiling == True:
        atexit.register(exit_handler)
    # BFS
    bfs_prof_start_time = time()
    best_cost = 999 # represent infinite
    best_node = None
    dq = deque()
    dq.append(game_tree.root)
    while len(dq) != 0:
        # profiling
        if len(dq) > bfs_prof_max_queue_size:
            bfs_prof_max_queue_size = len(dq)
        # profilingend

        node = dq.popleft() # the leftmost one
        # profiling
        bfs_prof_node_explored += 1
        if node.path_cost > bfs_prof_depth_reached:
            bfs_prof_depth_reached = node.path_cost
        # profiling end

        if node.point == game_tree.end_point:
            if node.path_cost < best_cost:
                best_cost = node.path_cost
                best_node = node
            break
        elif len(node.remain_num) == 0 :
            continue

        # add five children
        node.appendchildren()
        for ch_name in node.children.keys():
            child = node.children.get(ch_name, None)
            if child != None:
                dq.append(child)
    #end while
    
    # profiling
    bfs_prof_end_time = time()
    bfs_prof_execute_time = bfs_prof_end_time - bfs_prof_start_time
    # profiling end


    if show_profiling == True:
        bfs_show_profile()
    
    if best_node != None:
        return solution_path(best_node)
    else:
        return None