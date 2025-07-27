import type { Job } from "./jobs";

export type Result = {
    session_id: string;
    recommend: Job[];
    good: Job[];
    bad: Job[];
}

