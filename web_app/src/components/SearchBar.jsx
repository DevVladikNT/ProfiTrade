import axios from "axios";
import { Card, Flex, Title, TextInput, Button } from "@tremor/react";
import { useState } from "react";

function SearchBar(props) {
    const [string, setString] = useState('');

    const search = () => {
        const getData = async () => {
            const response_ = await axios.get('http://localhost:2000/search/' + string).catch((error) => {
                enqueueSnackbar(error, {variant: 'error'});
            });
            const company_ = response_.data.response[0];
            props.setResult(company_);
        };
        getData();
    };

    const onKeyDown= (event) => {
        if (event.key === 'Enter')
            search()
    }

    return (
        <Card className="mb-4 mt-4">
            <Title>Company:</Title>
            <Flex flexDirection="row">
                <TextInput
                    value={string}
                    onChange={(event) => setString(event.target.value)}
                    onKeyDown={onKeyDown}
                    placeholder="Name / Ticker / Figi"
                />
                <Button className="ml-4" onClick={search}>Search</Button>
            </Flex>
        </Card>
    );
}

export default SearchBar;