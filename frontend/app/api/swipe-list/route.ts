import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const session_id = searchParams.get('session_id')
  const res = await fetch(`${process.env.BACKEND_URL}/swipe-list?session_id=${session_id}`,{
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
  if (!res.ok) {
    return NextResponse.json({ error: 'Failed to get swipe list' }, { status: 500 })
  }
  const data = await res.json()
  return NextResponse.json(data);
}

