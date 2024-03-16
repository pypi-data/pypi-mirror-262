import React, { useEffect, useRef, useState } from "react";
import { AiOutlinePlusCircle } from "react-icons/ai";
import { MdDelete } from "react-icons/md";
import { FaChevronLeft } from "react-icons/fa";
import pdfIcon from "../../assets/pdf.svg";
import textIcon from "../../assets/text.svg";
import docxIcon from "../../assets/docs.svg";
import odtIcon from "../../assets/odt.png";
import wave from "../../images/wave.png";
import dots from "../../images/dots.png";
import folder from "../../assets/folder.svg";
import arrowLeft from "../../assets/arrowLeft.svg";
import { ApiPost } from "../../API/API_data";
import { API_Path } from "../../API/ApiComment";
import { Box, Modal } from "@mui/material";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: "fit-content",
  bgcolor: "background.paper",
  border: "none",
  boxShadow: 20,
  p: 4,
  borderRadius: "20px",
  outline: "none",
};

const ChatBotSideBar = ({
  uploadedFiles = [],
  setIsCollections,
  isCollections,
  setSelectedCollectionName,
  setSelectedFileName,
}) => {
  const user = JSON.parse(localStorage.getItem("komodoUser"));
  const fileInputRef = useRef(null);

  const [open, setOpen] = React.useState(false);

  const [collection, setCollection] = useState("");
  const [description, setDescription] = useState("");

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const collections = ["abc", "xyz", "dots", "dolor", "large text", "test folder"];
  const getFileIcon = (fileType) => {
    if (fileType.includes("pdf")) {
      return pdfIcon;
    } else if (fileType.includes("doc")) {
      return docxIcon;
    } else if (fileType.includes("text")) {
      return textIcon;
    } else {
      return odtIcon;
    }
  };

  const handleSelectItem = (name) => {
    setSelectedCollectionName(name);
  };

  const handleSelectedFileName = (name) => {
    setSelectedFileName(name);
  };

  // const handleButtonClick = () => {
  //   fileInputRef.current.click();
  // };

  const handleAddCollections = async () => {
    let body = {
      collection: collection,
      description: description,
    };
    try {
      const response = await ApiPost(API_Path.addCollection, body);
      if (response.ok) {
        // Handle success
        console.log("Collection added successfully");
        setOpen(false);
        setCollection("");
        setDescription("");
      } else {
        // Handle error
        console.error("Failed to add collection");
      }
    } catch (error) {
      console.error("Error occurred while adding collection:", error);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    // console.log("Uploaded file:", file);
  };

  // useEffect(() => {
  //   const handleOutsideClick = (e) => {
  //     if (showModal && !e.target.closest(".modal")) {
  //       setShowModal(false);
  //     }
  //   };

  //   document.body.addEventListener("click", handleOutsideClick);

  //   return () => {
  //     document.body.removeEventListener("click", handleOutsideClick);
  //   };
  // }, [showModal]);

  return (
    <div className="col-span-1 w-[100%]">
      <div className="mb-8">
        <h1 className="text-[21px] font-cerebri text-[#495057] leading-[27px] mb-9 mt-5 mx-5">
          AI assistant
        </h1>
        {isCollections ? (
          <div className="text-center">
            <button
              className="bg-[#316FF6] text-[#fff] rounded-md px-[75px] pb-2 pt-3 text-[15px] font-cerebriregular xxl:px-10"
              // onClick={(e) => {
              //   e.stopPropagation();
              //   handleOpenModal();
              // }}
              onClick={handleOpen}
            >
              New Collection
            </button>
            <input type="file" ref={fileInputRef} style={{ display: "none" }} onChange={handleFileChange} />
          </div>
        ) : (
          <div className="text-center">
            <button className="bg-[#316FF6] text-[#fff] rounded-md px-[75px] pb-2 pt-3 text-[15px] font-cerebriregular xxl:px-10">
              New Document
            </button>
          </div>
        )}
      </div>
      {isCollections ? (
        <>
          <div className="flex items-center justify-between pt-4 px-5 border-t-[0.5px] border-[#F6F6F9]">
            <div className="text-blackText text-[18px] mb-3 -ml-2 font-cerebriMedium">Collections</div>
          </div>
          <div>
            <div className="sidebar h-[calc(100vh-251px)] overflow-auto">
              {collections.map((item, index) => {
                return (
                  <div
                    className={`flex items-center justify-between px-3 py-2 mt-1 cursor-pointer overflow-hidden`}
                    onClick={() => handleSelectItem(item)}
                    key={index}
                  >
                    <div
                      key={index}
                      className={`flex items-center gap-2 cursor-pointer`}
                      onClick={() => setIsCollections(false)}
                    >
                      <span className="bg-customsky p-2 rounded-[5px]">
                        <img src={folder} className="w-5 h-5" alt="" />
                      </span>

                      <div>
                        <div className="text-blackText font-medium font-cerebri text-[14px] w-[110px] whitespace-nowrap overflow-hidden text-ellipsis">
                          {item}
                        </div>
                      </div>
                    </div>
                    <img src={dots} alt="dots" className="min-w-[16px]" />
                  </div>
                );
              })}
            </div>
          </div>
        </>
      ) : (
        <>
          <div className="py-3 px-5 flex flex-col gap-4 border-b border-customGray">
            <div
              className="text-blackText flex text-[18px] gap-2 -ml-2 font-cerebriMedium cursor-pointer "
              onClick={() => {
                setIsCollections(true);
                setSelectedFileName("");
              }}
            >
              <img src={arrowLeft} className="w-5 h-5" alt="" />
              Collection
            </div>
            <span className="text-blackText text-[18px] font-cerebriMedium -ml-2">Files</span>
          </div>

          <div>
            <div className="sidebar h-[calc(100vh-290px)] overflow-auto">
              {uploadedFiles.map((file, index) => {
                return (
                  <div
                    className={`flex items-center justify-between px-3 py-2 mt-1 cursor-pointer overflow-hidden`}
                    onClick={() => handleSelectedFileName(file.name)}
                    key={index}
                  >
                    <div key={index} className={`flex items-center gap-2`}>
                      <span className="bg-customsky p-2 rounded-[5px]">
                        <img src={getFileIcon(file.type)} alt="" className="w-5 h-5" />
                      </span>

                      <div>
                        <div className="text-blackText font-medium font-cerebri text-[14px] w-[110px] whitespace-nowrap overflow-hidden text-ellipsis">
                          {file.name}
                        </div>
                      </div>
                    </div>
                    <img src={dots} alt="dots" className="min-w-[16px]" />
                  </div>
                );
              })}
            </div>
            {/* <div className="mx-3">
              <div className="flex items-center gap-2 py-3">
                <AiOutlinePlusCircle className="text-blackText text-[20px]" />
                <div className="text-blackText font-normal font-cerebri text-[14px]">New document</div>
              </div>
            </div> */}
          </div>
        </>
      )}

      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <div className="font-cerebri text-[20px] text-[#3C3C3C] mb-4">Add Collection</div>

          <input
            type="text"
            placeholder="Add collection name..."
            className="bg-[#E0E8F8] rounded-lg w-full py-3 px-5 mb-4 font-cerebri border-none outline-none"
            value={collection}
            onChange={(e) => setCollection(e.target.value)}
          />
          <input
            type="text"
            placeholder="Add description..."
            className="bg-[#E0E8F8] rounded-lg w-full py-3 px-5 mb-4 font-cerebri border-none outline-none"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />

          <div className="flex items-center justify-end mt-4 gap-3">
            <button
              className="text-[18px] font-cerebriregular text-[#3C3C3C] border border-[#DDE8FF] rounded-lg py-2 px-5 shadow-drop cursor-pointer"
              onClick={handleClose}
            >
              Cancel
            </button>

            <button
              className="text-[18px] font-cerebriregular text-[#FFFFFF] bg-[#316FF6] rounded-lg py-2 px-7 cursor-pointer"
              onClick={handleAddCollections}
            >
              Add
            </button>
          </div>
        </Box>
      </Modal>
      <div className="mx-5 mb-3">
        <h1 className="text-[18px] leading-[25.4px] font-cerebri text-[#495057]">{user?.name}</h1>
      </div>
    </div>
  );
};

export default ChatBotSideBar;
