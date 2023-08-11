import { useState } from 'react'
import prodigyLogo from './assets/prodigy.svg'
import './App.css'

const API = "http://localhost/api/"

function App() {
    const [shortLink, setShortLink] = useState("")
    const [longLink, setLongLink] = useState("")
    const [isGood, setGood] = useState(true)

    let getShortLink = async () => {
        console.log(JSON.stringify({ "link": longLink }))
        if (longLink.trim() == "") return;
        let response = await fetch(API,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: JSON.stringify({ "link": longLink.trim() }),
            })
        if (response.ok) {
            let result = await response.json();
            setGood(true);
            setShortLink(result.short_url)
            console.log("OK")
        } else {
            setGood(false);
            console.log("Error")
        }
    }

    return (
        <>
            <div className="content">
                <div>
                    <img src={prodigyLogo} className="logo" alt="Prodigy logo" />
                </div>
                <h1>Prodigy</h1>
                <h3>URL Shortener</h3>
                <div className="create-link-form">
                    <input
                        type="text"
                        name="long-url"
                        id="long-url"
                        placeholder="Enter URL to shortify..."
                        className="create-link-field"
                        onChange={(e) => { setLongLink(e.target.value) }}
                    />
                    <button className="create-link-button" onClick={getShortLink}>Create link</button>
                </div>
                <div className="short-link">
                    {isGood ?
                        <div>
                            {shortLink ? <p className="short-link-text">Your's short link is:</p> : <p></p>}

                            <a href={shortLink}>{shortLink}</a>
                        </div>
                        :
                        <p>Something went wrong.</p>
                    }
                </div>
            </div>
            <footer>
                <a href="https://github.com/prodigy-by">Prodigy.by</a>
                &nbsp;&copy; 2023
            </footer>
        </>
    )
}

export default App
