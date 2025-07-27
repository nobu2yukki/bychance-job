import { NextResponse } from 'next/server';

export async function GET() {
  const res = await fetch(`${process.env.BACKEND_URL}/session/start`,{
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  })
  if (!res.ok) {
    return NextResponse.json({ error: 'Failed to start session' }, { status: 500 })
  }
  const data = await res.json()
  return NextResponse.json(data);
}