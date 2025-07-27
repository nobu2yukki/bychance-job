import { Question } from '@/types/question';
import { NextRequest, NextResponse } from 'next/server';

export async function GET() {
  const domain = process.env.BACKEND_URL;
  const res = await fetch(`${domain}/questions/all`);
  if (!res.ok) {
    console.log(res);
    return;
  }
  const questions: Question[] = await res.json();
  return NextResponse.json(questions);
}

export async function POST(request: NextRequest) {
  const domain = process.env.BACKEND_URL;
  const res = await fetch(`${domain}/questions/result`, {
    method: 'POST',
    body: JSON.stringify(request.json()),
  });
  if (!res.ok) {
    console.log(res);
    return;
  }
  const result = await res.json();
  return NextResponse.json(result);
}
