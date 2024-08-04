import { useState } from "react";
import { useEffect } from "react";
import { callApi } from "../api";

export default function Table() {
    const tableKeys = ["title", "start_year", "end_year", "intensity", "sector", "topic", "insight",
        "region", "impact", "added", "published", "country", "relevance", "pestle",
        "source", "likelihood"];
    function tableKeyToHead(key) {
        return key.split("_").map(word => word.charAt(0).toUpperCase() + word.substring(1)).join(' ');
    }
    const [filters, setFilters] = useState({});
    const [pageNo, setPageNo] = useState(1);
    const [records, setRecords] = useState([]);
    const [pageCount, setPageCount] = useState(10);
    const [totalPages, setTotalPages] = useState(10);
    function dataFetch(pageNo) {
        callApi('records', { 'page': pageNo, 'count': pageCount }, filters).then(response => {
            if (response.status == 200) {
                response.json().then(response_json => {
                    setPageNo(response_json.page);
                    setPageCount(response_json.count);
                    setTotalPages(response_json.total_pages);
                    setRecords(response_json.records);
                }).catch(console.error);
            } else {
                console.error(response);
            }
        }).catch(console.error);
    }
    useEffect(() => {
        dataFetch(pageNo);
    }, []);
    function onNextPage() {
        console.log(totalPages, pageNo);
        if ((pageNo + 1) <= totalPages) {
            setPageNo(pageNo + 1);
            dataFetch(pageNo + 1);
        } else if (pageNo != 1) {
            setPageNo(1);
            dataFetch(1);
        }
    }
    function onPrevPage() {
        console.log(totalPages, pageNo);
        if ((pageNo - 1) <= totalPages) {
            setPageNo(pageNo - 1);
            dataFetch(pageNo - 1);
        } else if (pageNo != totalPages) {
            setPageNo(totalPages);
            dataFetch(totalPages);
        }
    }
    return (
        <div className="relative overflow-x-auto">
            <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
                <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                    <tr>
                        {tableKeys.map(x => (
                            <th scope="col" key={x} className="px-4 py-3">
                                {tableKeyToHead(x)}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {records.map((record, id) => (
                        <tr key={id} className="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                            <th scope="row" className="px-4 py-4 text-gray-900 dark:text-white">
                                <a href={record.url} rel="nofollow noopener noreferrer" target="_blank">
                                    <svg width="24" height="24" fill="black" xmlns="http://www.w3.org/2000/svg" fillRule="evenodd" clipRule="evenodd">
                                        <path d="M14.851 11.923c-.179-.641-.521-1.246-1.025-1.749-1.562-1.562-4.095-1.563-5.657 0l-4.998 4.998c-1.562 1.563-1.563 4.095 0 5.657 1.562 1.563 4.096 1.561 5.656 0l3.842-3.841.333.009c.404 0 .802-.04 1.189-.117l-4.657 4.656c-.975.976-2.255 1.464-3.535 1.464-1.28 0-2.56-.488-3.535-1.464-1.952-1.951-1.952-5.12 0-7.071l4.998-4.998c.975-.976 2.256-1.464 3.536-1.464 1.279 0 2.56.488 3.535 1.464.493.493.861 1.063 1.105 1.672l-.787.784zm-5.703.147c.178.643.521 1.25 1.026 1.756 1.562 1.563 4.096 1.561 5.656 0l4.999-4.998c1.563-1.562 1.563-4.095 0-5.657-1.562-1.562-4.095-1.563-5.657 0l-3.841 3.841-.333-.009c-.404 0-.802.04-1.189.117l4.656-4.656c.975-.976 2.256-1.464 3.536-1.464 1.279 0 2.56.488 3.535 1.464 1.951 1.951 1.951 5.119 0 7.071l-4.999 4.998c-.975.976-2.255 1.464-3.535 1.464-1.28 0-2.56-.488-3.535-1.464-.494-.495-.863-1.067-1.107-1.678l.788-.785z" />
                                    </svg>
                                </a>
                                <span title={record.title}>{record.title}</span>
                            </th>
                            {tableKeys.slice(1).map(key => (
                                <td key={`${id}.${key}`} className="px-6 py-4">
                                    {record[key]}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
            <button onClick={onNextPage}>Next</button>
            <button onClick={onPrevPage}>Previous</button>
            <span>Current Page: {pageNo}</span>
        </div>
    );
}