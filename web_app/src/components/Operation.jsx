import axios from "axios";
import { Flex, Text, Title, NumberInput, Button, Metric, Divider } from "@tremor/react";
import { useEffect, useState } from "react";

function Operation({figi, price, amount}) {
    const [name, setName] = useState(figi);

    useEffect(() => {
        const getData = async () => {
            let response = await axios.get('http://localhost:2000/search/' + figi);
            let company_name = response.data.response[0].name;
            setName(company_name)
        };
        getData();
    }, []);

    return (
        <Flex flexDirection="col">
            <Divider>{name}</Divider>
            <Flex flexDirection="row">
                <Title>{price}</Title>
                <Text>{amount > 0 ? 'bought' : 'sold'} x{amount > 0 ? amount : -amount}</Text>
            </Flex>
        </Flex>
    );
}

export default Operation;