"use client";
import React from 'react'
import { loginaction } from './Loginfunc';

  const login = ()=>{
  return (
    <main className='flex items-center justify-center min-h-screen'>
  
      <form action={loginaction} className='flex flex-col gap-4'>
        <h1 className='text-center'>LOGIN </h1>
        <input type="email" name = "email" placeholder='Enter your email' required className='p-1 border' />
        <input type="password" name = "password" placeholder='Enter your password' required className='p-1 border' />
        <button type='submit' className='px-1'>Login</button>
      </form>

    </main>
  )
}

export default login