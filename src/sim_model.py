import simpy
import numpy as np

def run_sim(arrivals, nb_buses, capacity, boarding_time, trip_time, sim_time):
    """
    Runs the bus simulation.
    
    Args:
        arrivals: List of dicts [{'arrival_time': float, 'student_id': int}, ...]
        nb_buses: Number of buses
        capacity: Max students per bus
        boarding_time: Time to board one student (min)
        trip_time: Round trip time (min)
        sim_time: Total simulation duration (min)
        
    Returns:
        dict: Statistics (avg_wait, total_transported, etc.)
    """
    env = simpy.Environment()
    
    # State
    queue = []
    stats = {
        "wait_times": [],
        "students_transported": 0,
        "queue_over_time": [], # List of (time, length)
        "bus_utilization": [],
    }
    
    # --- Processes ---
    
    def student_generator(env, arrivals):
        """Generates students based on arrival data."""
        for p in arrivals:
            t_arrival = p['arrival_time']
            if t_arrival > sim_time:
                break
            
            # Wait until arrival time
            yield env.timeout(max(0, t_arrival - env.now))
            
            # Student joins queue
            queue.append({
                'id': p['student_id'],
                'arrival_time': env.now
            })
            stats['queue_over_time'].append((env.now, len(queue)))

    def bus_process(env, bus_id, start_delay):
        """Simulates a single bus loop."""
        yield env.timeout(start_delay)
        
        while True:
            # Bus arrives at stop
            
            # Boarding process
            boarded = 0
            while boarded < capacity and queue:
                student = queue.pop(0)
                
                # Record wait time
                wait_time = env.now - student['arrival_time']
                stats['wait_times'].append(wait_time)
                
                # Boarding takes time
                yield env.timeout(boarding_time)
                boarded += 1
            
            if boarded > 0:
                stats['students_transported'] += boarded
            
            # Record utilization
            stats['bus_utilization'].append(boarded / capacity)

            # Record queue state after boarding
            stats['queue_over_time'].append((env.now, len(queue)))
            
            # Drive / Round Trip
            yield env.timeout(trip_time)

    # --- Setup ---
    
    env.process(student_generator(env, arrivals))
    
    # Stagger bus starts evenly
    interval = trip_time / nb_buses if nb_buses > 0 else trip_time
    for i in range(nb_buses):
        env.process(bus_process(env, i, start_delay=i * interval))
        
    # --- Run ---
    env.run(until=sim_time)
    
    # --- Results ---
    avg_wait = np.mean(stats['wait_times']) if stats['wait_times'] else 0.0
    avg_util = np.mean(stats['bus_utilization']) if stats['bus_utilization'] else 0.0
    return {
        "avg_wait_time": avg_wait,
        "avg_bus_utilization": avg_util,
        "total_transported": stats['students_transported'],
        "queue_over_time": stats['queue_over_time'],
        "raw_wait_times": stats['wait_times']
    }
