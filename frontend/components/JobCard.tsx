import type { Job } from '@/types/jobs';
import Image from 'next/image';

interface JobCardProps {
  job: Job;
}

export default function JobCard({ job }: JobCardProps) {
  return (
    <div className="w-full h-full bg-white rounded-2xl shadow-xl overflow-hidden cursor-grab active:cursor-grabbing flex flex-col">
      <div className="relative h-40 flex-shrink-0">
        <Image
          src={job.image_url}
          alt={job.company_name}
          fill
          className="object-cover"
          draggable={false}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
        <div className="absolute top-2 right-2">
          <span className="inline-block bg-blue-500 text-white px-2 py-1 rounded-full text-xs font-medium">
            {job.category.parent} / {job.category.child}
          </span>
        </div>
      </div>
      <div className="p-4 flex-1 flex flex-col bg-transparent">
        <h1 className="text-xl font-extrabold mb-2 line-clamp-1">
          {job.company_name}
        </h1>
        <div className="flex items-center justify-between mb-3">
          <span className="font-semibold text-base">
            {job.salary}
          </span>
          <p className="text-gray-500 text-xs">📍 {job.place}</p>
        </div>
        <p className="text-gray-700 text-xs mb-3 flex-shrink-0">
          {job.description}
        </p>
        <div className="space-y-2">
          <div>
            <p className="text-xs text-gray-500 font-medium mb-1">🧑‍💻 働き方</p>
            <div className="flex flex-wrap gap-1">
              {job.work_style.slice(0, 2).map((work_style) => (
                <span
                  key={work_style}
                  className="bg-green-50 text-green-700 px-2 py-1 rounded-full text-xs border border-green-200"
                >
                  {work_style}
                </span>
              ))}
            </div>
          </div>
          <div>
            <p className="text-xs text-gray-500 font-medium mb-1">🎁 福利厚生</p>
            <div className="flex flex-wrap gap-1">
              {job.audience.slice(0, 2).map((audience) => (
                <span
                  key={audience}
                  className="bg-yellow-50 text-yellow-700 px-2 py-1 rounded-full text-xs border border-yellow-200"
                >
                  {audience}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}