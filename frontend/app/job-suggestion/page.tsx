"use client";

import { Accordion } from "@/components/Accordion";
import JobCard from "@/components/JobCard";
import RankCrown from "@/components/RankCrown";
import { sampleJobs } from "@/mock_data/jobs";
import type { Job } from "@/types/jobs";
import type { SwipeResultWithJob } from "@/types/swipe_results";
import Link from "next/link";
import { useEffect, useState } from "react";


export default function Home() {
  const [suggestJobs, setSuggestJobs] = useState<Job[]>([]);
  const [choicedJob, setChoicedJob] = useState<SwipeResultWithJob>();
  useEffect(() => {
    const fetchSuggestJobs = async () => {
      return sampleJobs
    }
    fetchSuggestJobs().then(jobs => setSuggestJobs(jobs));
    const fetchChoicedJob = async () => {
      return {
        good: sampleJobs.slice(0, 3),
        bad: sampleJobs.slice(3, 6)
      }
    }
    fetchChoicedJob().then(jobs => setChoicedJob(jobs));
  }, []);

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-6">
        <h2 className="text-center text-xl sm:text-2xl font-bold my-3 sm:my-5">
          あなたにマッチした求人の一覧
        </h2>
        <p className="text-center text-sm sm:text-base mb-6">
          あなたにマッチした求人数の一覧
        </p>
        {choicedJob && (
          <Accordion items={[{ title: '🙆 あなたが興味のある求人', content: choicedJob.good.map((job) => <JobCard key={job.id} job={job} />) }]} allowMultiple={false} />
        )}
        {choicedJob && (
          <Accordion items={[{ title: '🙅 あなたの興味のない求人', content: choicedJob.bad.map((job) => <JobCard key={job.id} job={job} />) }]} allowMultiple={false} />
        )}
        <hr className="my-4" />
        <div className="space-y-4 sm:space-y-6 mb-8">
          {suggestJobs.map((job, rank: number) => (
            <div key={job.id} className="flex flex-col gap-2">
              <RankCrown rank={rank + 1} size={36} />
              <JobCard key={job.id} job={job} />
            </div>
          ))}
        </div>
        <div className="text-center">
          <Link href="/">
            <button className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200 w-full sm:w-auto" type="button">
              トップページへ
            </button>
          </Link>
        </div>
      </div>
    </main >
  );
}