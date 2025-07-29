"use client";

import { Accordion } from "@/components/Accordion";
import JobCard from "@/components/JobCard";
import RankCrown from "@/components/RankCrown";
import { useSession } from "@/contexts/SessionContext";
import type { Job } from "@/types/jobs";
import type { Result } from "@/types/results";
import type { SwipeResultWithJob } from "@/types/swipe_results";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function Home() {
  const [result, setResult] = useState<Result>();
  const [suggestJobs, setSuggestJobs] = useState<Job[]>([]);
  const [choicedJob, setChoicedJob] = useState<SwipeResultWithJob>();
  const { sessionId } = useSession();
  const router = useRouter();
  useEffect(() => {
    const fetchResult = async () => {
      try {
        const res = await fetch(`/api/results?session_id=${sessionId}`);
        const data = await res.json();
        setResult(data);
      setSuggestJobs(data?.recommend || []);
      setChoicedJob({
        good: data?.good || [],
        bad: data?.bad || []
      });
    } catch (error) {
      alert('Failed to get result');
      router.push('/');
    }
  }
  fetchResult()
  }, [sessionId, router]);

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
          <Accordion items={[{ title: '🙆 あなたが興味のある求人', content: choicedJob.good.map((job) => <JobCard key={`good-${job.id}`} job={job} />) }]} allowMultiple={false} />
        )}
        {choicedJob && choicedJob.bad.length > 0 && (
          <Accordion items={[{ title: '🙅 あなたの興味のない求人', content: choicedJob.bad.map((job) => <JobCard key={`bad-${job.id}`} job={job} />) }]} allowMultiple={false} />
        )}
        <hr className="my-4" />
        <div className="space-y-4 sm:space-y-6 mb-8">
          {suggestJobs.map((job, rank: number) => (
            <div key={`suggest-${job.id}`} className="flex flex-col gap-2">
              <RankCrown rank={rank + 1} size={36} />
              <JobCard job={job} />
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