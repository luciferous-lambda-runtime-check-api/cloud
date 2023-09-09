def handler(event:, context:)
    [
        "AWS_EXECUTION_ENV=#{ENV['AWS_EXECUTION_ENV']}",
        "VERSION=#{RUBY_VERSION}"
    ].join("&c")
end