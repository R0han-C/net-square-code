from datetime import datetime
import sys

def parse_log_entry(line):
    try:
        time_str, username, action = line.strip().split()
        time_obj = datetime.strptime(time_str, "%H:%M:%S")
        if action.upper() not in ("START", "END"):
            return None
        return time_obj, username, action.upper()
    except ValueError:
        return None

def calculate_fair_billing(log_file):
    user_sessions = {}
    active_sessions = {}
    min_time = None
    max_time = None

    with open(log_file, 'r') as f:
        for line in f:
            parsed_entry = parse_log_entry(line)
            if parsed_entry is None:
                continue

            time_obj, username, action = parsed_entry

            if min_time is None:
                min_time = time_obj
            max_time = time_obj

            if action == "START":
                if username not in user_sessions:
                    user_sessions[username] = (0, 0)
                active_sessions[username] = time_obj
            elif action == "END":
                if username in active_sessions:
                    start_time = active_sessions.pop(username)
                    session_duration = (time_obj - start_time).total_seconds()
                    user_sessions[username] = (
                        user_sessions.get(username, (0, 0))[0] + 1,
                        user_sessions.get(username, (0, 0))[1] + session_duration
                    )
                else:
                    user_sessions[username] = (
                        user_sessions.get(username, (0, 0))[0] + 1,
                        user_sessions.get(username, (0, 0))[1] + (time_obj - min_time).total_seconds()
                    )

    for username, start_time in active_sessions.items():
        session_duration = (max_time - start_time).total_seconds()
        user_sessions[username] = (
            user_sessions.get(username, (0, 0))[0] + 1,
            user_sessions.get(username, (0, 0))[1] + session_duration
        )

    return user_sessions

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    log_file = sys.argv[1]
    result = calculate_fair_billing(log_file)

    for username, (sessions, total_duration) in result.items():
        print(f"{username} {sessions} {int(total_duration)}")

if __name__ == "__main__":
    main()
