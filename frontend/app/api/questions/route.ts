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
  const searchParams = request.nextUrl.searchParams;
  const session_id = searchParams.get('session_id');
  const body = await request.json();
  console.log(body);
  const domain = process.env.BACKEND_URL;
  const res = await fetch(
    `${process.env.BACKEND_URL}/questions/result?session_id=${session_id}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    },
  );
  if (!res.ok) {
    console.log(res);
    return NextResponse.json(
      { error: 'Failed to send question result' },
      { status: 500 },
    );
  }
  const result = await res.json();
  return NextResponse.json(result);
}
