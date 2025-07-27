'use client';

import JobCardWrapper from '@/app/job-match/JobCardWrapper';
import { useSession } from '@/contexts/SessionContext';
import type { Job } from '@/types/jobs';
import type { SwipeResult } from '@/types/swipe_results';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function Home() {
  const router = useRouter();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [swipeResult, setSwipeResult] = useState<SwipeResult>({
    good: [],
    bad: [],
  });

  const { sessionId } = useSession();

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const res = await fetch(`/api/swipe-list?session_id=${sessionId}`);
        const swipe_list = await res.json();
        return swipe_list;
      } catch (error) {
        alert('Failed to get swipe list');
        router.push('/');
        return;
      }
    };

    fetchJobs().then(jobs => {
      if (jobs) { // jobsが存在する場合のみsetJobsを実行
        setJobs(jobs);
      }
    });
  }, [sessionId, router]);


  const handleSwipe = (jobId: number, status: 'good' | 'bad') => {
    console.log(jobId, status);
    setSwipeResult(prev => {
      const newSwipeResult = { ...prev };
      newSwipeResult[status] = [...newSwipeResult[status], jobId];
      return newSwipeResult;
    });
  };

  // データの送信
  const handleComplete = async (jobId: number, status: 'good' | 'bad') => {
    const finalResult = (() => {
      const newSwipeResult = { ...swipeResult };
      newSwipeResult[status] = [...newSwipeResult[status], jobId];
      return newSwipeResult;
    })();

    const body = {
      session_id: sessionId,
      ...finalResult
    }
    const res = await fetch(`/api/swipe-result`, {
      method: 'POST',
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      alert('Failed to send swipe result');
      router.push('/');
      return;
    }

    setTimeout(() => {
      router.push('/job-suggestion');
    }, 3000);
  };

  return (
    <main>
      <JobCardWrapper jobs={jobs} handleSwipe={handleSwipe} handleComplete={handleComplete} />
    </main>
  );
}