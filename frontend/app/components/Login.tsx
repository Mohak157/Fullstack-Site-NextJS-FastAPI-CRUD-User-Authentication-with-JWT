"use client";
import React,{useState,ChangeEvent} from 'react';
import { useRouter } from 'next/navigation';



  const Login = ()=>{
     const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleLogin = async (e:React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();

    const response = await fetch("http://localhost:8000/auth/jwt/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        username: email,
        password: password,
      }),
    });

    if (!response.ok) {
      alert("Invalid credentials");
      return;
    }

    const data = await response.json();
    localStorage.setItem("access_token", data.access_token);

    router.push("/feed");
  };


    return (
    <main className='flex items-center justify-center min-h-screen'>
  
      <form onSubmit={handleLogin} className='flex flex-col gap-4'>
        <h1 className='text-center'>LOGIN </h1>
        <input type="email" value={email}  onChange={(e)=>setEmail(e.target.value)} name = "email" placeholder='Enter your email' required className='p-1 border' />
        <input type="password" value={password} onChange ={(e)=>setPassword(e.target.value)} name = "password" placeholder='Enter your password' required className='p-1 border' />
        <button type='submit' className='px-1'>Login</button>
      </form>

    </main>
  )
}

export default Login