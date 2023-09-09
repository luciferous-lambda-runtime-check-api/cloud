exports.handler = async (_event) => {
    return [
        `AWS_EXECUTION_ENV=${process.env.AWS_EXECUTION_ENV}`,
        `VERSION=${process.versions.node}`
    ].join("&")
};