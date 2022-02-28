import React from "react"


export default MyList = (nItems) => {
    let items = [...Array(nItems)].map((_, i) => <li>{`Item ${i}`}</li>)
    return <ul>{items}</ul>
}
