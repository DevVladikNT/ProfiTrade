import axios from "axios";
import { Flex, Text, Title, Divider } from "@tremor/react";
import { useEffect, useState } from "react";

function Operation(props) {
    const [name, setName] = useState(props.figi);

    useEffect(() => {
        const getData = async () => {
            const response = await axios.get('http://localhost:2000/search/' + props.figi);
            const company_name = response.data.response[0].name;
            setName(company_name);
        };
        getData();
    }, []);

    return (
        <Flex flexDirection="col">
            <Divider>{name}</Divider>
            <Flex flexDirection="row">
                <Text>{props.amount > 0 ? 'bought' : 'sold'} x{props.amount > 0 ? props.amount : -props.amount}</Text>
                <Title>{props.price}</Title>
            </Flex>
        </Flex>
    );
}

export default Operation;