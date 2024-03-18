import React from 'react'
import { Link } from 'react-router-dom'
import { GoArrowRight } from "react-icons/go";
import chatimg from '../../src/images/chatimg.png'
import content from '../../src/images/content.png'
import user from '../../src/images/user.png'
import copy from '../../src/images/copy.png'
import summary from '../../src/images/summary.png'
import first from '../../src/images/first.png'
import second from '../../src/images/second.png'
import chatgpt from '../../src/images/chatgpt.png'
import tick from '../../src/images/tick.png'

const Home = () => {
    return (
        <div>
            <div
                className="bg-cover bg-no-repeat bg-center px-[100px] xl:px-[60px] lg:px-[40px] sm:px-3 sm:py-3"
                style={{ backgroundImage: "url('/home.png')" }}
            >
                <div className="flex items-center sm:flex-col py-7 w-full justify-between">
                    <h1 className="text-3xl font-cerebrisemibold ">Komodo AI</h1>
                    <div className='flex gap-14'>
                        <p className='text-[#316FF6] text-[20px] font-cerebriregular leading-[24px]'>Home</p>
                        <Link to='/pricing'>
                            <p className='text-[#333333] text-[20px] font-cerebriregular leading-[24px]'>Pricing</p>
                        </Link>
                    </div>
                    <div className="flex gap-6 sm:justify-end sm:gap-3">
                        <div className="flex gap-3">
                            <Link to='/login'>
                                <button className="bg-[#F3F7FF] text-[18px] font-cerebri border text-customBlue border-[#C7D8FD] py-2 px-4 rounded-[10px] min-w-[107px]">
                                    Login
                                </button>
                            </Link>
                            <Link to='/signup'>
                                <button className="bg-customBlue text-[18px]  font-cerebri py-2 px-5 text-white rounded-[10px] min-w-[113px]">
                                    Sign up
                                </button>
                            </Link>
                        </div>
                    </div>
                </div>
                <div className='pt-7 flex justify-center items-center flex-col'>
                    <h2 className='text-[#316FF6] text-[18px] font-cerebriMedium leading-[24px]'>Contis.ai MAKES CONTENT FAST & EASY</h2>
                    <h1 className='text-[#1E2B45] text-[78px] font-cerebribold leading-[24px] mt-12'>Write content 10x faster</h1>
                    <p className='text-[#797C8C] text-[18px] font-cerebriregular leading-[31px] mt-10'>Using advanced artificial intelligence and deep learning, Article Forge writes</p>
                    <p className='text-[#797C8C] text-[18px] font-cerebriregular leading-[31px]'> entire 1,500+ word articles automatically. From product descriptions.</p>
                    <button className='flex justify-center items-center w-fit gap-2 text-[#ffffff] text-[20px] font-cerebri leading-[24px] bg-[#316FF6] rounded-md px-8 pt-4 pb-3 mt-8'>Try Komodo AI <GoArrowRight /></button>
                </div>
                <div className='mt-10'>
                    <img src={content} alt="content" className='absolute bottom-96' />
                    <div className='flex justify-center mt-14'>
                        <img src={chatimg} alt="chatimg" />
                    </div>
                    <img src={user} alt="user" className='absolute bottom-24 right-20' />
                </div>

            </div>

            <div className='mt-20 flex justify-center items-center flex-col'>
                <div className='flex justify-center items-center flex-col leading-[24px]'>
                    <h2 className='text-[#316FF6] text-[18px] font-cerebri'>PRICING</h2>
                    <h1 className='text-[#000000] text-[48px] font-cerebri mt-7'>Instruct to our AI writing generate copy</h1>
                    <p className='text-[#797C8C] text-[16px] font-cerebriregular mt-8'>Let our AI assist with most time consuming to write blog articles,</p>
                    <p className='text-[#797C8C] text-[16px] font-cerebriregular'>  product descriptions and more.</p>
                </div>
                <div className='flex bg-[#EEF5FF] rounded-3xl w-fit mt-12 px-20 pt-16 pb-10'>
                    <img src={copy} alt="copy" />
                    <div className='ps-20'>
                        <img src={first} alt="first" className='mt-14' />
                        <h1 className='text-[#000000] text-[38px] font-cerebri leading-[48px] mt-8 mb-3'>Generate copy in <br /> seconds</h1>
                        <p className='text-[#797C8C] text-[16px] font-cerebriregular leading-[27px]'>Generate many types of content in under 30 seconds by <br /> simply inserting a few input fields. Generate blog topic <br /> ideas, intros, ad copy, copywriting.</p>
                        <button className='flex justify-center items-center w-fit text-[#ffffff] text-[18px] font-cerebri leading-[24px] bg-[#316FF6] rounded-md px-6 pt-4 pb-3 mt-8'>Get Started</button>
                    </div>
                </div>
                <div className='flex bg-[#F1F1FF] rounded-3xl w-fit mt-12 px-20 pt-16 pb-10'>
                    <div className='pe-20'>
                        <img src={second} alt="second" className='mt-14' />
                        <h1 className='text-[#000000] text-[38px] font-cerebri leading-[48px] mt-8 mb-3'>Summarize PowerPoint <br /> presentations and more</h1>
                        <p className='text-[#797C8C] text-[16px] font-cerebriregular leading-[27px]'>Use our AI to create presentations for you. Simply <br /> upload a document and ask SlideSpeak to generate a <br /> presentation based on the content.</p>
                        <button className='flex justify-center items-center w-fit text-[#ffffff] text-[18px] font-cerebri leading-[24px] bg-[#316FF6] rounded-md px-6 pt-4 pb-3 mt-8'>Get Started</button>
                    </div>
                    <img src={summary} alt="summary" />
                </div>
            </div>

            <div className='flex justify-center items-center mt-6 px-20 pt-16 pb-10'>
                <img src={chatgpt} alt="chatgpt" />
                <div className='ps-20 flex flex-col justify-center'>
                    <p className='text-[#316FF6] text-[18px] font-cerebri leading-[24px]'>Komodo AI HELP YOU TO CREATE CONTENT FAST</p>
                    <h1 className='text-[#000000] text-[38px] font-cerebri leading-[58px] mt-6 mb-3'>As sleek as ChatGPT, but with the<br /> finesse of your documents."</h1>
                    <p className='text-[#797C8C] text-[16px] font-cerebriregular leading-[24px]'>Upload your Any Type documents and ask questions about the content.</p>
                    <div className='flex gap-3 items-center mt-12'><img src={tick} alt="tick" /><span className='text-[#3C3C3C] text-[20px] font-cerebriregular leading-[24px]'>Create brief descriptions</span></div>
                    <div className='flex gap-3 items-center mt-7'><img src={tick} alt="tick" /><span className='text-[#3C3C3C] text-[20px] font-cerebriregular leading-[24px]'>Create presentations</span></div>
                    <div className='flex gap-3 items-center mt-7'><img src={tick} alt="tick" /><span className='text-[#3C3C3C] text-[20px] font-cerebriregular leading-[24px]'>Feel free to inquire about absolutely anything...</span></div>
                </div>
            </div>

            <div className='py-20 mt-3' style={{ backgroundImage: "url('/faqbg.png')" }}>
                <div className='flex justify-center items-center flex-col leading-[24px]'>
                    <h2 className='text-[#316FF6] text-[18px] font-cerebri'>FAQ</h2>
                    <h1 className='text-[#000000] text-[48px] font-cerebri mt-7'>Frequently asked question</h1>
                    <p className='text-[#797C8C] text-[16px] font-cerebriregular mt-8'>Please feel free to reach out to us. We are always happy to assist you and provide any additional.</p>
                </div>
            </div>
        </div>
    )
}

export default Home