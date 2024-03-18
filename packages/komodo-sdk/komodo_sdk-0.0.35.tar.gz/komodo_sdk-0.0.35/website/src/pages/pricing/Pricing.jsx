import React from "react";
import bluetick from "../../assets/blueTick.svg";
import { Link } from "react-router-dom";
const Pricing = () => {
  const firstCard = [
    "Up to 50 Files",
    "Monthly questions limit",
    "Invite team members",
    "New feature early access",
    "Customer support",
    "Max file size",
    "1000 Visiters",
  ];
  return (
    <div
      className="font-cerebriregular bg-cover bg-no-repeat bg-center"
      style={{ backgroundImage: "url('/pricingBg.png')" }}
    >
      <div className="px-[100px] xl:px-[60px] pt-7 lg:px-[40px] sm:px-3 sm:py-3">
        <div className="flex justify-between items-center sm:flex-col">
          <h1 className="text-3xl font-cerebrisemibold">Komodo AI</h1>
          <div className="flex justify-between items-center gap-6 sm:justify-end sm:gap-3">
            <p>Pricing</p>
            <div className="flex gap-3">
              <Link to='/login'>
                <button className="bg-[#F3F7FF] border text-customBlue border-[#C7D8FD] py-2 px-4 rounded-[10px] min-w-[107px]">
                  Login
                </button>
              </Link>
              <Link to='/chat'>
                <button className="bg-customBlue py-2 px-5 text-white rounded-[10px] min-w-[113px]">
                  Try Now
                </button>
              </Link>
            </div>
          </div>
        </div>
        <div className="pb-7 h-[calc(100vh-70px)] overflow-auto scrollbar">
          <div className="text-center pt-16 pb-20 flex flex-col gap-2 w-[600px] m-auto sm:w-[370px]">
            <h5 className="text-customBlue text-[18px] font-medium">PRICING</h5>
            <h1 className="text-[34px] font-cerebribold">Choose your plan</h1>
            <div>
              <p className="text-[#797C8C] text-[16px] pb-1">
                Boost your productivity and use our AI tools to summarize Word
                documents
                {/* </p>
            <p className="text-[#797C8C] text-[16px]"> */}
                PDF and PowerPoint presentations and more.
              </p>
            </div>
            <div className="flex justify-center gap-4 items-center">
              <p>Monthly</p>

              <label className="inline-flex items-center cursor-pointer">
                <input type="checkbox" value="" className="sr-only peer" />
                <div className="relative w-12 h-7 bg-white peer-focus:outline-none rounded-full peer dark:bg-white peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white peer-checked:after:bg-white after:content-[''] after:absolute after:top-[4px] after:start-[2px] after:bg-customBlue after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
              </label>
              <p className="text-[#797C8C]">Yearly</p>
              <div className="rounded-[43px] text-customBlue border border-customBlue px-3 py-1">
                20% OFF
              </div>
            </div>
          </div>
          <div className="flex lg:flex-wrap xl:gap-5 lg:gap-10 gap-10 justify-center items-end md:flex-col md:items-center">
            <div className="border border-[#C7D8FD] w-[307px] h-[784] rounded-[26px] bg-white p-[46px]">
              <h2 className="text-[20px] font-cerebriMedium text-center">Starter</h2>
              <h1 className="text-[34px] font-cerebriMedium text-center">
                $48
                <span className="text-[16px] text-[#797C8C] font-cerebri">
                  / MO
                </span>
              </h1>
              <div className="my-5">
                {firstCard?.map((item) => {
                  return (
                    <div className="flex items-center gap-3">
                      <img src={bluetick} className="w-[17px] h-[11px]" />
                      <p className="text-[#3C3C3C]">{item}</p>
                    </div>
                  );
                })}
              </div>

              <button className="bg-customBlue py-2 px-5 text-white rounded-[10px] w-full ">
                Get started
              </button>
            </div>
            <div className="border border-[#C7D8FD] w-[307px] h-[800] rounded-[26px] text-white bg-[#1E2B45] ">
              <div className="bg-customBlue p-2 rounded-t-[26px] text-center">
                Most Popular
              </div>
              <div className="p-[46px]">
                <h2 className="text-[20px] font-cerebriMedium text-center">Starter</h2>
                <h1 className="text-[34px] font-cerebriMedium text-center">
                  $48
                  <span className="text-[16px]  font-cerebri">
                    / MO
                  </span>
                </h1>
                <div className="my-5">
                  {firstCard?.map((item) => {
                    return (
                      <div className="flex items-center gap-3">
                        <img src={bluetick} className="w-[17px] h-[11px]" />
                        <p className="">{item}</p>
                      </div>
                    );
                  })}
                </div>

                <button className="bg-customBlue py-2 px-5 text-white rounded-[10px] w-full ">
                  Get started
                </button>
              </div>

            </div>
            <div className="border border-[#C7D8FD] w-[307px] h-[784] rounded-[26px] bg-white p-[46px]">
              <h2 className="text-[20px] font-cerebriMedium text-center">Enterprice</h2>
              <h1 className="text-[34px] font-cerebriMedium text-center">
                Custom
                {/* <span className="text-[16px] text-[#797C8C] font-cerebri">
                / MO
              </span> */}
              </h1>
              <div className="my-5">
                {firstCard?.map((item) => {
                  return (
                    <div className="flex items-center gap-3">
                      <img src={bluetick} className="w-[17px] h-[11px]" />
                      <p className="text-[#3C3C3C]">{item}</p>
                    </div>
                  );
                })}
              </div>

              <button className="bg-customBlue py-2 px-5 text-white rounded-[10px] w-full ">
                Get started
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Pricing;

