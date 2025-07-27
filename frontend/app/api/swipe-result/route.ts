import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const body = await request.json()
  console.log(body)
  const res = await fetch(`${process.env.BACKEND_URL}/swipe-results`,{
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    console.log(res)
    return NextResponse.json({ error: 'Failed to send swipe result' }, { status: 500 })
  }
  const data = await res.json()
  return NextResponse.json(data);
}