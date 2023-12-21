import axios from "axios";
import { Flex, Text, Title, Divider } from "@tremor/react";
import { useEffect, useState } from "react";

function Operation(props) {

    const date = new Date(props.time * 1000);

    return (
        <Flex flexDirection="col">
            <Divider />
            <Flex flexDirection="row">
                <Text>{props.amount > 0 ? 'bought' : 'sold'} x{props.amount > 0 ? props.amount : -props.amount}</Text>
                <Title>{props.price}</Title>
            </Flex>
            <Flex flexDirection="row">
                <Text>
                    {date.toLocaleDateString('en-US', { day: 'numeric' })}.
                    {date.toLocaleDateString('en-US', { month: 'numeric' })}. 
                    {date.toLocaleDateString('en-US', { year: 'numeric' })}
                </Text>
                <Text>
                    {date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                </Text>
            </Flex>
        </Flex>
    );
}

export default Operation;