import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import { BiMinus } from "react-icons/bi";
import menuIcon from "../assets/Frame.svg";
import Drawer from "react-modern-drawer";
import close from "../assets/close.svg";
import { FiPlus, FiSearch, FiXCircle } from "react-icons/fi";
import ChatBotSideBar from "../components/chatBot/ChatBotSideBar";
import { Chat } from "../components/chatBot/Chat";
import HeaderSideBar from "../components/HeaderSideBar";
import pdf from "../images/sample.pdf";
import DocViewer, { DocViewerRenderers } from "@cyntler/react-doc-viewer";
import Header from "../components/Header";

const ChatBot = () => {
  // "https://nett.umich.edu/sites/default/files/docs/pdf_files_scan_create_reducefilesize.pdf"
  // "https://medicine-storage.s3.ap-southeast-2.amazonaws.com/pdfs/p9973001.pdf"
  const docs = [{ uri: pdf }];
  const uploadedFiles = [
    {
      lastModified: "2024-03-04, 10:30",
      name: "document1.pdf",
      type: "pdf",
      file: "path/to/document1.pdf",
      key: "unique_key_1",
    },
    {
      lastModified: "2024-03-04, 10:30",
      name: "image1.docs",
      type: "docs",
      file: "path/to/image1.docs",
      key: "unique_key_2",
    },
    {
      lastModified: "2024-03-04, 10:30",
      name: "spreadsheet1.text",
      type: "text",
      file: "path/to/spreadsheet1.text",
      key: "unique_key_3",
    },
    {
      lastModified: "2024-03-04, 10:30",
      name: "document1.pdf",
      type: "pdf",
      file: "path/to/document1.pdf",
      key: "unique_key_1",
    },
    {
      lastModified: "2024-03-04, 10:30",
      name: "image1.docs",
      type: "docs",
      file: "path/to/image1.docs",
      key: "unique_key_2",
    },
    {
      lastModified: "2024-03-04, 10:30",
      name: "spreadsheet1.text",
      type: "text",
      file: "path/to/spreadsheet1.text",
      key: "unique_key_3",
    },
  ];

  const [isCollections, setIsCollections] = useState(true);
  const [searchText, setSearchText] = useState("");
  const [isSearchVisible, setIsSearchVisible] = useState(false);
  const [numPages, setNumPages] = useState(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [selectedCollectionName, setSelectedCollectionName] = useState("");
  const [selectedFileName, setSelectedFileName] = useState("");

  const toggleDrawer = () => {
    setIsDrawerOpen(!isDrawerOpen);
  };

  return (
    <div className="flex lg:block">
      <img
        src={menuIcon}
        className="hidden xl:flex w-[24px] h-[24px] m-3"
        onClick={toggleDrawer}
        alt=""
      />

      <div className="xl:hidden w-1/5 font-cerebri flex border-r-[0.5px] border-[#CDCDCD]">
        <Sidebar />
        <ChatBotSideBar
          uploadedFiles={uploadedFiles}
          setIsCollections={setIsCollections}
          isCollections={isCollections}
          setSelectedCollectionName={setSelectedCollectionName}
          setSelectedFileName={setSelectedFileName}
        />
      </div>

      <Drawer
        open={isDrawerOpen}
        onClose={toggleDrawer}
        direction="left"
        className="chatDrawer"
      >
        <Sidebar />
        <div className="font-cerebri w-[-webkit-fill-available] flex flex-col justify-between">
          <img
            src={close}
            className="w-[14px] h-[14px] absolute right-3 top-5"
            onClick={toggleDrawer}
            alt=""
          />

          <ChatBotSideBar
            uploadedFiles={uploadedFiles}
            setIsCollections={setIsCollections}
            isCollections={isCollections}
            setSelectedCollectionName={setSelectedCollectionName}
            setSelectedFileName={setSelectedFileName}
          />
        </div>
      </Drawer>

      <div className="col-span-6 h-screen xl:w-full w-4/5">
        <Header />
        <div className="grid lg:grid-cols-1 grid-cols-2">
          <div className="col-span-1 xl:border-l xl:border-[#E8E9EA]">
            <Chat
              selectedItemName={selectedCollectionName}
              selectedFileName={selectedFileName}
            />
          </div>

          <div className="col-span-1 border-l border-[#E8E9EA]">
            {
              isCollections
                ? // <HeaderSideBar />
                  ""
                : ""
              // <div className="flex items-center justify-between py-[19px] px-3 border-b border-[#E8E9EA]">
              //   <div className="flex items-center gap-4">
              //     <div className="text-[#1C232D] font-cerebri font-normal text-[16px]">
              //       <span className="bg-[#F2F4FE] px-3 py-1 rounded-lg">1</span> / 4
              //     </div>
              //   </div>

              //   <div className="flex items-center lg:gap-1 gap-3">
              //     <FiPlus className="text-[18px] cursor-pointer" />
              //     <div className="text-[#1C232D] text-[16px] font-cerebri font-normal bg-[#F2F4FE] rounded py-1/2 px-1">
              //       100%
              //     </div>
              //     <BiMinus className="text-[18px] cursor-pointer" />
              //   </div>

              //   <div className="flex items-center gap-2 relative">
              //     {isSearchVisible && (
              //       <input
              //         type="text"
              //         className="border md:hidden border-[#EEEFEF] py-[3px] -mt-1 -mb-1 px-4 rounded-lg outline-none text-[#808DA4] text-[16px] font-cerebriregular font-normal"
              //         placeholder="search"
              //         value={searchText}
              //         onChange={(e) => setSearchText(e.target.value)}
              //       />
              //     )}

              //     {searchText && isSearchVisible && (
              //       <span
              //         className="md:hidden absolute text-blackText right-8 top-1/2 transform -translate-y-1/2 cursor-pointer"
              //         onClick={() => setSearchText("")}
              //       >
              //         <FiXCircle className="text-[#A4A7AB] text-[20px]" />
              //       </span>
              //     )}

              //     <FiSearch
              //       className="text-[#A4A7AB] text-[20px] cursor-pointer"
              //       onClick={() => setIsSearchVisible(!isSearchVisible)}
              //     />
              //   </div>
              // </div>
            }

            <div
              className={`bg-[#FFFFFF] ${
                isCollections ? "" : "h-[calc(100vh-93px)]"
              }`}
            >
              <DocViewer
                pluginRenderers={DocViewerRenderers}
                documents={docs}
                config={{
                  header: {
                    disableHeader: false,
                    disableFileName: true,
                    retainURLParams: false,
                  },
                }}
                // style={{ width: 500, height: 500 }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatBot;
