#include <cstdio>
#include <iostream>
#include <vector>
#include <sstream>
#include <queue>
#include <map>

bool startsWith(const std::string& haystack, const std::string& needle) {
    return haystack.find(needle) == 0;
}

typedef std::pair<std::pair<int, int>, std::string> taskArgs;

enum taskType {
    TASK_PRINT,
    TASK_SEND,
    TASK_RECEIVE
};

const int D = 1;

typedef std::vector<int> TimeStamp;

std::map<taskArgs, TimeStamp> message_pool;

void printTimestamp(const TimeStamp& t) {
    std::cout << " [";
    for(auto& num : t) {
        std::cout << " " << num;
    }
    std::cout << " ]";
}

class Task {
    private:
        taskType type;
        taskArgs args;

    public:
        Task(taskType type, taskArgs& args) {
            this->type = type;
            this->args = args;
        }

        bool execute(TimeStamp& timestamp) {
            switch (type) {
                case TASK_PRINT:
                    std::cout << "printed p" << args.first.first << " " << args.second;
                    printTimestamp(timestamp);
                    std::cout << std::endl;
                    break;
                case TASK_SEND:
                    message_pool.insert({args, timestamp});
                    std::cout << "sent p" << args.first.first << " " << args.second << " p" << args.first.second;
                    printTimestamp(timestamp);
                    std::cout << std::endl;
                    break;
                case TASK_RECEIVE:
                    if (message_pool.find(args) == message_pool.end()) {
                        return false;
                    } else {

                        for (int i = 0; i < timestamp.size(); ++i) {
                            timestamp[i] = std::max(timestamp[i], message_pool[args][i]);
                        }

                        message_pool.erase(args);
                        std::cout << "received p" << args.first.first << " " << args.second << " p" << args.first.second;
                        printTimestamp(timestamp);
                        std::cout << std::endl;
                    }
                    break;
            }
            return true;
        }
};

class Process {
    private:
        int index;
        TimeStamp timestamp;
        std::queue<Task> events;

    public:
        Process(int index) {
            this->index = index;
            this->timestamp = TimeStamp(9, 0);
        }

        void add_event(taskType type, taskArgs args) {
            events.push({type, args});
        }

        int events_left() const {
            return events.size();
        }

        bool run() {
            bool did_run = false;
            if (!events.empty()) {
                timestamp[index - 1] += D;
                bool t = events.front().execute(timestamp);
                if (t) {
                    events.pop();
                    did_run = true;
                } else {
                    timestamp[index - 1] -= D;
                }
            }
            return did_run;
        }

};

int main(void) {

    std::vector<Process> sites;

    std::string inp;
    int currentProcessIndex = -1;
    while(std::getline(std::cin, inp)) {
        if (inp != "") {
            if (startsWith(inp, "begin process p")) {
                int idx = -1;
                if (sscanf(inp.c_str(), "begin process p%d", &idx) != 1) {
                    std::cerr << "Error reading process number from line: " << inp << std::endl;
                    exit(1);
                }
                currentProcessIndex = idx;
                sites.push_back(idx);

            } else if (startsWith(inp, "send p")) {
                std::stringstream ss(inp);
                std::string curr;
                getline(ss, curr, ' ');
                if (!getline(ss, curr, ' ')) {
                    std::cerr << "Error reading process number from line: " << inp << std::endl;
                    exit(1);
                }

                int idx = -1;
                if (sscanf(curr.c_str(), "p%d", &idx) != 1) {
                    std::cerr << "Error reading process number from line: " << inp << std::endl;
                    exit(1);
                }

                if (!getline(ss, curr)) {
                    std::cerr << "Error reading message from line: " << inp << std::endl;
                    exit(1);
                }


                sites.back().add_event(TASK_SEND, {{currentProcessIndex, idx}, curr});

            } else if (startsWith(inp, "recv p")) {
                std::stringstream ss(inp);
                std::string curr;
                getline(ss, curr, ' ');
                if (!getline(ss, curr, ' ')) {
                    std::cerr << "Error reading process number from line: " << inp << std::endl;
                    exit(1);
                }

                int idx = -1;
                if (sscanf(curr.c_str(), "p%d", &idx) != 1) {
                    std::cerr << "Error reading process number from line: " << inp << std::endl;
                    exit(1);
                }

                if (!getline(ss, curr)) {
                    std::cerr << "Error reading message from line: " << inp << std::endl;
                    exit(1);
                }

                sites.back().add_event(TASK_RECEIVE, {{idx, currentProcessIndex}, curr});

            } else if (startsWith(inp, "print ")) {
                std::stringstream ss(inp);
                std::string curr;
                getline(ss, curr, ' ');
                if (!getline(ss, curr)) {
                    std::cerr << "Error reading message from line: " << inp << std::endl;
                    exit(1);
                }
                sites.back().add_event(TASK_PRINT, {{currentProcessIndex, -1}, curr});

            } else if (startsWith(inp, "end process")) {
                currentProcessIndex = -1;
            } else {
                std::cerr << "Unknown input format for line: " << inp << std::endl;
                exit(1);

            }
        }
    }

    bool did_run = true;
    while(did_run) {
        did_run = false;
        for (auto& it: sites) {
            did_run |= it.run();
        }
    }


    if (message_pool.size() != 0) {
        for (auto& it : sites) {
            if (it.events_left() != 0) {
                std::cerr << "system deadlocked" << std::endl;
                break;
            }
        }
    }

    return 0;
}

