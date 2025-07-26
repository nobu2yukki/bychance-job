import { Job } from "./jobs";

export type SwipeResult = {
    good: number[];
    bad: number[];
};

export type SwipeResultWithJob = {
    good: Job[];
    bad: Job[];
};